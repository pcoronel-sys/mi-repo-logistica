import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="App Logística", layout="wide")

# Conexión mejorada
conn = st.connection("gsheets", type=GSheetsConnection)

# ... (resto de tu código de títulos y pestañas igual) ...

def procesar_carga(nombre_seccion, worksheet_name):
    st.header(f"Sección de {nombre_seccion}")
    archivo = st.file_uploader(f"Subir Excel para {nombre_seccion}", type=["xlsx"], key=f"up_{worksheet_name}")
    
    if archivo:
        df_nuevo = pd.read_excel(archivo)
        if st.button(f"Confirmar y Actualizar {nombre_seccion}", key=f"btn_{worksheet_name}"):
            try:
                # Intentamos la actualización
                conn.update(worksheet=worksheet_name, data=df_nuevo)
                st.success("¡Datos actualizados!")
                st.cache_data.clear() # Limpia la memoria para ver los cambios
            except Exception as e:
                st.error("Error de permisos: Google no permite escribir con un link público. Necesitas configurar los 'Secrets' con el formato completo.")
                st.info("Mira el Paso 2 que te envié en el chat.")

    # Al leer, usamos ttl=0 para que siempre traiga lo más nuevo de Google
    try:
        df_actual = conn.read(worksheet=worksheet_name, ttl=0)
        st.dataframe(df_actual)
    except:
        st.info("Pestaña vacía.")
