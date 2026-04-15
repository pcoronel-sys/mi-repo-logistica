import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="App Logística Cloud", layout="wide")

# Conectar con Google Sheets
# Nota: La URL se configura en la siguiente sección
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("📂 Repositorio en la Nube (Google Sheets)")

tab1, tab2, tab3 = st.tabs(["🔄 EXTRACICLOS", "📅 REPROGRAMACIONES", "📦 BULTOS"])

def gestionar_seccion(nombre_pestaña, worksheet_name):
    st.header(f"Sección {nombre_pestaña}")
    
    # 1. Subir archivo
    archivo = st.file_uploader(f"Actualizar {nombre_pestaña}", type=["xlsx"], key=nombre_pestaña)
    
    if archivo:
        df_nuevo = pd.read_excel(archivo)
        if st.button(f"Subir a Google Sheets - {nombre_pestaña}"):
            # Esto escribe los datos en la pestaña correspondiente de Google
            conn.update(worksheet=worksheet_name, data=df_nuevo)
            st.success("¡Datos guardados en la nube!")

    st.divider()

    # 2. Leer datos actuales
    try:
        df_actual = conn.read(worksheet=worksheet_name)
        st.subheader("Datos actuales en Google Sheets:")
        st.dataframe(df_actual)
    except:
        st.warning("Aún no hay datos en esta pestaña.")

with tab1:
    gestionar_seccion("Extraciclos", "Extraciclos")
with tab2:
    gestionar_seccion("Reprogramaciones", "Reprogramaciones")
with tab3:
    gestionar_seccion("Bultos", "Bultos")
