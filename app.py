import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Repo Logística", layout="wide")

st.title("📂 Repositorio Logística")

# Intentar la conexión
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    st.success("Conexión con Google establecida")
except Exception as e:
    st.error(f"Error de conexión: {e}")

tab1, tab2, tab3 = st.tabs(["EXTRACICLOS", "REPROGRAMACIONES", "BULTOS"])

def cargar(titulo, sheet_name):
    with st.container():
        st.subheader(titulo)
        archivo = st.file_uploader(f"Subir {titulo}", type=['xlsx'], key=sheet_name)
        
        if archivo:
            df = pd.read_excel(archivo)
            if st.button(f"Guardar {titulo}"):
                conn.update(worksheet=sheet_name, data=df)
                st.success("Guardado en Google Sheets")
        
        st.divider()
        # Mostrar lo que hay
        try:
            df_actual = conn.read(worksheet=sheet_name, ttl=0)
            st.dataframe(df_actual)
        except:
            st.info("Sin datos previos.")

with tab1: cargar("Extraciclos", "Extraciclos")
with tab2: cargar("Reprogramaciones", "Reprogramaciones")
with tab3: cargar("Bultos", "Bultos")
