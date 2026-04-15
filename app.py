import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración inmediata
st.set_page_config(page_title="Carga Logística", layout="wide")

st.title("📂 Repositorio Logística")

# 2. Conexión protegida
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Error al conectar con Google: {e}")
    st.stop() # Detiene la ejecución si no hay conexión

# 3. Interfaz de pestañas
tab1, tab2, tab3 = st.tabs(["EXTRACICLOS", "REPROGRAMACIONES", "BULTOS"])

def procesar(nombre, hoja):
    st.subheader(f"Gestión de {nombre}")
    
    # Subida de archivo
    archivo = st.file_uploader(f"Excel para {nombre}", type=["xlsx"], key=f"key_{hoja}")
    
    if archivo:
        try:
            df = pd.read_excel(archivo)
            st.write("Vista previa:")
            st.dataframe(df.head(3))
            
            if st.button(f"Guardar en {nombre}", key=f"btn_{hoja}"):
                conn.update(worksheet=hoja, data=df)
                st.success("¡Datos guardados!")
                st.cache_data.clear()
        except Exception as e:
            st.error(f"Error procesando archivo: {e}")

    st.divider()
    
    # Mostrar datos
    try:
        data = conn.read(worksheet=hoja, ttl=0)
        st.dataframe(data, use_container_width=True)
    except:
        st.info(f"Sin datos en la pestaña {hoja}")

with tab1: procesar("Extraciclos", "Extraciclos")
with tab2: procesar("Reprogramaciones", "Reprogramaciones")
with tab3: procesar("Bultos", "Bultos")
