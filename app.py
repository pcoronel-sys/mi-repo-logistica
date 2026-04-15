import streamlit as st
import pandas as pd
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Repositorio Web de Datos", layout="wide")

# Crear carpeta de datos si no existe
if not os.path.exists("data"):
    os.makedirs("data")

# --- 2. FUNCIONES DE AYUDA ---
def procesar_archivo(nombre_seccion, clave_uploader):
    """Maneja la subida y visualización de archivos"""
    st.header(f"Gestión de {nombre_seccion}")
    
    # Subidor de archivos
    archivo = st.file_uploader(f"Arrastra aquí el Excel de {nombre_seccion}", type=["xlsx"], key=clave_uploader)
    
    if archivo:
        df = pd.read_excel(archivo)
        st.success(f"✅ Archivo '{archivo.name}' cargado con éxito.")
        
        # Botón para guardar
        if st.button(f"Actualizar Repositorio de {nombre_seccion}"):
            df.to_csv(f"data/{nombre_seccion}.csv", index=False)
            st.balloons()
            st.info(f"Los datos de {nombre_seccion} han sido actualizados para este mes.")

    st.divider()
    
    # Mostrar datos guardados
    path_guardado = f"data/{nombre_seccion}.csv"
    if os.path.exists(path_guardado):
        st.subheader("📋 Información actual en el sistema")
        datos_actuales = pd.read_csv(path_guardado)
        st.dataframe(datos_actuales, use_container_width=True)
    else:
        st.warning("Aún no hay datos cargados para esta categoría.")

# --- 3. INTERFAZ DE USUARIO (PÁGINA WEB) ---
st.title("📂 Repositorio de Carga Mensual")
st.markdown("Bienvenido al sistema de actualización de inventarios y logística.")

# Crear las pestañas que funcionan como el menú de tu web
tab1, tab2, tab3 = st.tabs(["🔄 EXTRACICLOS", "📅 REPROGRAMACIONES", "📦 BULTOS"])

with tab1:
    procesar_archivo("Extraciclos", "up_extra")

with tab2:
    procesar_archivo("Reprogramaciones", "up_repro")

with tab3:
    procesar_archivo("Bultos", "up_bultos")
