import datetime
from _plotly_utils.colors.plotlyjs import Rainbow
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Dashboard de Compras/Ventas", layout="wide", page_icon="icon.png")

# -----------------------------
# Cargar archivo desde sesión o subida
# -----------------------------
st.sidebar.header(f":rainbow[Gestión de Datos]", divider="rainbow")

uploaded_file = st.sidebar.file_uploader("Subir archivo data.csv", type=["csv"], help="Recuerda pulsar en la X luego de añadir el archivo para que la table sea editable")
timestamp = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
file_name = f"data_{timestamp}.csv"

# si no existe df en session_state lo creamos vacío
if "df" not in st.session_state:
    st.session_state["df"] = pd.DataFrame(columns=[
        "item", "fecha_compra", "precio_compra", "fecha_venta", "precio_venta", "ganancia"
    ])

# si el usuario sube archivo, lo cargamos
if uploaded_file is not None:
    st.session_state["df"] = pd.read_csv(uploaded_file)

df = st.session_state["df"]

st.sidebar.download_button(
    "Descargar data.csv",
    data=st.session_state["df"].to_csv(index=False),
    file_name=file_name,
    mime="text/csv",
    help="Se creará un archivo data.csv en tu almacenamiento"
)


st.title(":rainbow[Dashboard de Compras y Ventas]")

# ------------------------------------
# Formulario para Añadir nuevo ítem
# ------------------------------------
with st.container(border=True):
    st.subheader(":rainbow[Añadir nuevo ítem]", divider="rainbow")

    col1, col2 = st.columns(2, border=True)

    # Inputs dinámicos
    item = col1.text_input("Item")
    precio_compra = col1.number_input("Precio de compra", min_value=0.0, value=0.0)
    fecha_compra = col1.date_input("Fecha de compra")
    precio_venta = col2.number_input("Precio de venta (opcional)", min_value=0.0)
    fecha_venta = col2.date_input("Fecha de venta (opcional)", value=None)

    # Ganancia dinámica
    ganancia = precio_venta - precio_compra
    col2.number_input("Ganancia", value=ganancia)

    # Botón de añadir
    if st.button("Añadir", width="stretch"):
        new_row = {
            "item": item,
            "fecha_compra": str(fecha_compra),
            "precio_compra": precio_compra,
            "precio_venta": precio_venta if precio_venta > 0 else None,
            "fecha_venta": str(fecha_venta) if precio_venta > 0 else None,
            "ganancia": ganancia
        }

        df.loc[len(df)] = new_row   
        df = df.reset_index(drop=True)
        st.session_state["df"] = df

        st.success("Ítem añadido correctamente")

# ------------------------------------
# Tabla editable
# ------------------------------------
st.subheader(":rainbow[Tabla de datos]", divider="rainbow")

# Convertir fechas
df["fecha_compra"] = pd.to_datetime(df["fecha_compra"], errors="coerce")
df["fecha_venta"] = pd.to_datetime(df["fecha_venta"], errors="coerce")

# Botón ordenar
if st.button("Ordenar tabla por fecha de compra"):
    df = df.sort_values("fecha_compra", ascending=True)
    st.session_state["df"] = df
    st.success("Tabla ordenada por fecha de compra")

# Editor
edited_df = st.data_editor(df, num_rows="dynamic")

# -----------------
# Vaciar la tabla
# ------------------
b1,b2=st.columns(2)
with b1:
    st.download_button(
        "Descargar .csv",
        data=st.session_state["df"].to_csv(index=False),
        file_name=file_name,
        width="stretch",
        mime="text/csv",
        help="Se creará un archivo data.csv en tu almacenamiento"
    )
with b2:
    if st.button(
        "Vaciar Tabla",
        width="stretch",
        help="Recuerda quitar el archivo subido para que surtan los cambios"
    ):
        st.session_state["df"] = st.session_state["df"].iloc[0:0].copy()
        st.success("Tabla vaciada correctamente")
        st.rerun()

# ------------------------------------
# Totales estadísticos
# ------------------------------------
total_gastado = df["precio_compra"].sum()
total_vendido = pd.to_numeric(df["precio_venta"], errors="coerce").sum()
total_beneficio = df["ganancia"].astype(float).sum()

color = "green" if total_beneficio >= 0 else "red"
st.sidebar.write("---")
show_ganancia=st.sidebar.title(f":{color}[Ganancia]")
show_ganancia=st.sidebar.subheader(
    f"**:{color}[{total_beneficio} CUP]**",
    divider="rainbow"
    )

# ------------------------------------
# Gráfico grande resumen
# ------------------------------------
if len(df) > 0:

    with st.container(border=True):
        st.subheader(":rainbow[Resumen general]", divider="rainbow")

        resumen_df = pd.DataFrame({
            "Categoría": ["Gastado", "Ingresos por ventas", "Beneficio total"],
            "Cantidad (CUP)": [total_gastado, total_vendido, total_beneficio]
        })

        fig_resumen_bar = px.bar(
            resumen_df,
            x="Categoría",
            y="Cantidad (CUP)",
            text="Cantidad (CUP)"
        )

        fig_resumen_bar.update_traces(marker_color=["#e74c3c", "#2ecc71", "#3498db"])
        fig_resumen_bar.update_layout(height=450)

        st.plotly_chart(fig_resumen_bar, width="stretch")

    with st.container(border=True):
        # ============================
        # GANANCIAS Y PÉRDIDAS POR MES
        # ============================

        df_month = df.copy()

        df_month["precio_compra"] = pd.to_numeric(df_month["precio_compra"], errors="coerce")
        df_month["precio_venta"] = pd.to_numeric(df_month["precio_venta"], errors="coerce")
        df_month["ganancia"] = pd.to_numeric(df_month["ganancia"], errors="coerce")

        # Caso 1: items vendidos → usar fecha_venta
        df_month["mes"] = df_month["fecha_venta"].dt.to_period("M").astype(str)

        # Caso 2: items NO vendidos → usar fecha_compra y contar pérdida temporal
        mask_no_sale = df_month["precio_venta"].isna()

        df_month.loc[mask_no_sale, "ganancia"] = -df_month.loc[mask_no_sale, "precio_compra"]
        df_month.loc[mask_no_sale, "mes"] = (
            df_month.loc[mask_no_sale, "fecha_compra"]
            .dt.to_period("M")
            .astype(str)
        )

        # Agrupar por mes
        df_month_summary = df_month.groupby("mes", as_index=False)["ganancia"].sum()

        # Clasificar
        df_month_summary["Resultado"] = df_month_summary["ganancia"].apply(
            lambda x: "Ganancia" if x >= 0 else "Pérdida"
        )

        # Gráfico
        fig_mes = px.bar(
            df_month_summary,
            x="mes",
            y="ganancia",
            color="Resultado",
            #title="Ganancias y Pérdidas por Mes",
            color_discrete_map={"Ganancia": "green", "Pérdida": "red"},
            text="ganancia"
        )

        fig_mes.update_layout(
            xaxis_title="Mes",
            yaxis_title="Ganancia / Pérdida (CUP)",
            font=dict(size=14)
        )

        st.subheader(":rainbow[Ganancias / Pérdidas Mensuales]", divider="rainbow")
        st.plotly_chart(fig_mes, width="stretch")


    # -------------------------------------
    # Gráficos individuales
    # -------------------------------------
    st.subheader(":rainbow[Gráficos por Item]", divider="rainbow")

    colg1, colg2 = st.columns(2, border=True)

    # --------------------------------------
    # Gráfico de ganancias
    # --------------------------------------

    # Crear un DF temporal para no alterar el original
    df_copy=df.copy()
    df_copy["Resultado"] = df_copy["ganancia"].astype(float).apply(
        lambda x: "Ganancia" if x > 0 else "Pérdida"
    )

    fig_ganancia = px.bar(
        df_copy,
        x="item",
        y="ganancia",
        color="Resultado",
        color_discrete_map={"Ganancia": "green", "Pérdida": "red"},
        title="Ganancia / Pérdida por Item",
        category_orders={"item": df_copy["item"].tolist()} # para que mantengan el orden de la tabla
    )
    fig_ganancia.update_layout(
    xaxis_title="Item",
    yaxis_title="Ganancia/Pérdida (CUP)",
    font=dict(size=14)
    )
    
    colg1.plotly_chart(fig_ganancia, width="stretch")

    # Compra vs venta - convertir a formato long-form
    # Preparar datos: asegurar que ambas columnas sean numéricas
    df_cv = df.copy()
    df_cv["precio_compra"] = pd.to_numeric(df_cv["precio_compra"], errors="coerce")
    df_cv["precio_venta"] = pd.to_numeric(df_cv["precio_venta"], errors="coerce")

    
    # Convertir a formato long-form para Plotly
    df_melted = pd.melt(
        df_cv,
        id_vars=["item"],
        value_vars=["precio_compra", "precio_venta"],
        var_name="Tipo",
        value_name="Precio"
    )
    
    # Renombrar
    df_melted["Tipo"] = df_melted["Tipo"].replace({
        "precio_compra": "Precio Compra",
        "precio_venta": "Precio Venta"
    })
    
    fig_cv = px.line(
        df_melted,
        x="item",
        y="Precio",
        color="Tipo",
        title="Precio Compra vs Venta",
        color_discrete_map={"Precio Compra": "red", "Precio Venta": "green"},
    )

    fig_cv.update_traces(
        line=dict(width=3),
        mode="markers+text"
    )
    
    fig_cv.update_traces(
        selector=dict(name="Precio Compra"),
        marker=dict(symbol="triangle-down", size=12)
    )

    fig_cv.update_traces(
        selector=dict(name="Precio Venta"),
        marker=dict(symbol="triangle-up", size=12)
    )


    fig_cv.update_layout(
        xaxis_title="Item",
        yaxis_title="Precio (CUP)",
        font=dict(size=14)  
    )

    colg2.plotly_chart(fig_cv, width="stretch")

else:
    st.info("Añade datos para ver los gráficos.")
