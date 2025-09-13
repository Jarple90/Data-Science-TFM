# python -m streamlit run "Año 2024 Presupuestos\Interfaz\visor_streamlit.py"
import streamlit as st
import pandas as pd
import os
import importlib.util
import plotly.express as px

st.set_page_config(page_title="Presupuestos Serie Roja", layout="wide")
st.title("📊 Visor de Presupuestos - Serie Roja")

# Ruta base
ruta_base = r"R:\Data Science TFM\Año 2024 Presupuestos\Serie Roja"

# Modo de análisis
modo = st.radio("Modo de análisis", ["🔍 Sección única", "📊 Comparar dos secciones"])

# Función para cargar archivo .py o .csv
def cargar_archivo(ruta_archivo):
    df = None
    if ruta_archivo.endswith(".py"):
        try:
            spec = importlib.util.spec_from_file_location("modulo_presupuesto", ruta_archivo)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            for nombre in dir(modulo):
                objeto = getattr(modulo, nombre)
                if isinstance(objeto, pd.DataFrame):
                    df = objeto
                    break
        except Exception as e:
            st.error(f"Error al importar el archivo .py: {e}")
    elif ruta_archivo.endswith(".csv"):
        try:
            df = pd.read_csv(ruta_archivo, encoding="latin1", sep=";")
            df.fillna('', inplace=True)
        except Exception as e:
            st.error(f"Error al leer el archivo CSV: {e}")
    return df

# 🔍 Modo individual
if modo == "🔍 Sección única":
    secciones = [d for d in os.listdir(ruta_base) if os.path.isdir(os.path.join(ruta_base, d))]
    seccion = st.selectbox("Selecciona una sección", secciones)

    tipos_documento = ["Estado de Gastos", "Resumen Económico", "Resumen Orgánico"]
    tipo = st.radio("Selecciona el tipo de documento", tipos_documento)

    ruta_documento = os.path.join(ruta_base, seccion, tipo)
    archivos = [f for f in os.listdir(ruta_documento) if f.endswith(".csv") or f.endswith(".py")]
    archivo_seleccionado = st.selectbox("Selecciona un archivo", archivos)
    ruta_archivo = os.path.join(ruta_documento, archivo_seleccionado)

    df = cargar_archivo(ruta_archivo)

    if df is not None:
        st.success(f"✅ Archivo cargado: {archivo_seleccionado}")
        st.dataframe(df)

        columnas_numericas = df.select_dtypes(include="number").columns.tolist()
        columnas_categoricas = df.select_dtypes(exclude="number").columns.tolist()

        st.markdown("### 📋 Agrupación y resumen")
        col_agrupacion = st.selectbox("Agrupar por columna", columnas_categoricas)
        col_valor = st.selectbox("Sumar por columna", columnas_numericas)

        if col_agrupacion and col_valor:
            try:
                df_agrupado = df.groupby(col_agrupacion)[col_valor].sum().reset_index()
                st.dataframe(df_agrupado)

                st.markdown("### 📊 Gráfico de barras")
                fig_bar = px.bar(df_agrupado, x=col_agrupacion, y=col_valor, title=f"{col_valor} por {col_agrupacion}")
                st.plotly_chart(fig_bar, use_container_width=True)

                st.markdown("### 📈 Gráfico de líneas")
                fig_line = px.line(df_agrupado, x=col_agrupacion, y=col_valor, markers=True)
                st.plotly_chart(fig_line, use_container_width=True)
            except Exception as e:
                st.error(f"Error al agrupar o graficar: {e}")
        else:
            st.warning("Selecciona columnas válidas para agrupar y sumar.")

        st.markdown("### 🔍 Filtro por valor")
        filtro_columna = st.selectbox("Filtrar por columna", columnas_categoricas)
        opciones = df[filtro_columna].unique().tolist()
        seleccion = st.multiselect("Selecciona valores", opciones, default=opciones[:1])
        df_filtrado = df[df[filtro_columna].isin(seleccion)]
        st.dataframe(df_filtrado)

# 📊 Modo comparativo
elif modo == "📊 Comparar dos secciones":
    secciones = [d for d in os.listdir(ruta_base) if os.path.isdir(os.path.join(ruta_base, d))]
    secciones_seleccionadas = st.multiselect("Selecciona dos secciones para comparar", secciones, max_selections=2)

    if len(secciones_seleccionadas) != 2:
        st.warning("Selecciona exactamente dos secciones para activar la comparación.")
    else:
        tipo = st.radio("Selecciona el tipo de documento", ["Estado de Gastos", "Resumen Económico", "Resumen Orgánico"])
        dfs = []

        for seccion in secciones_seleccionadas:
            ruta_documento = os.path.join(ruta_base, seccion, tipo)
            archivos = [f for f in os.listdir(ruta_documento) if f.endswith(".csv") or f.endswith(".py")]

            if archivos:
                archivo = archivos[0]  # Tomamos el primero por simplicidad
                ruta_archivo = os.path.join(ruta_documento, archivo)
                df = cargar_archivo(ruta_archivo)

                if df is not None:
                    df["Sección"] = seccion
                    dfs.append(df)
                else:
                    st.error(f"No se pudo cargar datos de {seccion}")

        if len(dfs) == 2:
            df_comparado = pd.concat(dfs, ignore_index=True)

            columnas_numericas = df_comparado.select_dtypes(include="number").columns.tolist()
            columnas_categoricas = df_comparado.select_dtypes(exclude="number").columns.tolist()

            st.markdown("### 📋 Comparación agrupada")
            col_agrupacion = st.selectbox("Agrupar por", [c for c in columnas_categoricas if c != "Sección"])
            col_valor = st.selectbox("Sumar por", columnas_numericas)

            if col_agrupacion and col_valor:
                try:
                    df_agrupado = df_comparado.groupby(["Sección", col_agrupacion])[col_valor].sum().reset_index()
                    st.dataframe(df_agrupado)

                    st.markdown("### 📊 Gráfico comparativo por sección")
                    fig = px.bar(df_agrupado, x=col_agrupacion, y=col_valor, color="Sección", barmode="group",
                                title=f"{col_valor} por {col_agrupacion} en cada sección")
                    st.plotly_chart(fig, use_container_width=True)

                    st.markdown("### 📈 Evolución por sección")
                    fig_line = px.line(df_agrupado, x=col_agrupacion, y=col_valor, color="Sección", markers=True)
                    st.plotly_chart(fig_line, use_container_width=True)
                except Exception as e:
                    st.error(f"Error al agrupar o graficar: {e}")
            else:
                st.warning("Selecciona columnas válidas para agrupar y sumar.")

st.markdown("---")
st.markdown(
    "<div style='text-align: right;'>🧑‍💻 <strong>Autor:</strong> José Antonio Romero Pérez· 🗓️ Proyecto TFM · 📍 Málaga</div>",
    unsafe_allow_html=True)

