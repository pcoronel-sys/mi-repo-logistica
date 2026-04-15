import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Repositorio Logística", layout="wide")

# Conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📂 Sistema de Carga de Información Logística")
st.markdown("Carga tus archivos mensuales aquí. Los datos se guardarán automáticamente en Google Sheets.")

# Definir las pestañas
tab1, tab2, tab3 = st.tabs(["🔄 EXTRACICLOS", "📅 REPROGRAMACIONES", "📦 BULTOS"])

def procesar_carga(nombre_seccion, worksheet_name):
    st.header(f"Sección de {nombre_seccion}")
    
    # Subir el archivo Excel
    archivo = st.file_uploader(f"Subir Excel para {nombre_seccion}", type=["xlsx"], key=f"up_{worksheet_name}")
    
    if archivo:
        df_nuevo = pd.read_excel(archivo)
        st.write("🔍 Vista previa de los nuevos datos:")
        st.dataframe(df_nuevo.head(10))
        
        if st.button(f"Confirmar y Actualizar {nombre_seccion}", key=f"btn_{worksheet_name}"):
            with st.spinner('Actualizando Google Sheets...'):
                # Actualiza la pestaña específica en Google Sheets
                conn.update(worksheet=worksheet_name, data=df_nuevo)
                st.success(f"✅ ¡Datos de {nombre_seccion} actualizados correctamente!")
                st.balloons()

    st.divider()
    
    # Mostrar datos actuales
    try:
        st.subheader(f"📊 Datos actuales en {nombre_seccion}")
        df_actual = conn.read(worksheet=worksheet_name)
        st.dataframe(df_actual, use_container_width=True)
    except Exception:
        st.info(f"La pestaña '{worksheet_name}' está vacía o no existe aún en el Excel.")

# Ejecutar la lógica en cada pestaña
with tab1:
    procesar_carga("Extraciclos", "Extraciclos")

with tab2:
    procesar_carga("Reprogramaciones", "Reprogramaciones")

with tab3:
    procesar_carga("Bultos", "Bultos")
