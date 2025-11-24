import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Dashboard de Compras/Ventas", layout="wide", page_icon="icon.png")

# -----------------------------
# Cargar archivo desde sesión o subida
# -----------------------------
st.sidebar.header("Gestión de Datos", divider="rainbow")

uploaded_file = st.sidebar.file_uploader("Subir archivo data.csv", type=["csv"], help="Recuerda pulsar en la X luego de añadir el archivo para que la table sea editable")
timestamp = datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
file_name = f"data_{timestamp}.csv"

# si no existe df en session_state lo creamos vacío
if "df" not in st.session_state:
    st.session_state["df"] = pd.DataFrame(columns=[
        "item","tipo", "fecha_compra", "precio_compra", "fecha_venta", "precio_venta", "ganancia"
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


st.title("Dashboard de Compras y Ventas")

# ------------------------------------
# Formulario para Añadir nuevo ítem
# ------------------------------------
with st.container(border=True):
    st.subheader("Añadir Artículo", divider="rainbow")

    col1, col2 = st.columns(2, border=True)
    tipos = [
        "Configuración/Kit", "CPU", "Fuente de alimentación",
        "Cable", "Monitor", "Chasis", "RAM", "HDD", "SDD", "M2"
    ]
    # Inputs dinámicos
    item = col1.text_input("Item")
    tipo = col1.selectbox("Tipo", tipos)
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
            "tipo": tipo,
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
st.subheader("Tabla de Datos", divider="rainbow")

df["fecha_compra"] = pd.to_datetime(df["fecha_compra"], errors="coerce")
df["fecha_venta"] = pd.to_datetime(df["fecha_venta"], errors="coerce")

# ======================================
# Detectar items sin vender por +30 días
# ======================================

today = pd.Timestamp.today()
df["dias_desde_compra"] = (today - df["fecha_compra"]).dt.days
df["stuck"] = (df["fecha_venta"].isna()) & (df["dias_desde_compra"] >= 30)

# Editor con resaltado
edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    column_config={
        "stuck": st.column_config.CheckboxColumn(
            "Item estancado (+30 días sin vender)",
            help="Este producto lleva más de un mes guardado sin venderse.",
            disabled=True
        )
    },
    hide_index=True,
)

# Actualizar sesión
st.session_state["df"] = edited_df
df = edited_df

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

# Inversión actual = solo ítems NO vendidos
df_no_vendidos = df[df["fecha_venta"].isna()]
inversion_actual = df_no_vendidos["precio_compra"].sum()

ganancia_items_vendidos = df[df["fecha_venta"].notna()]["ganancia"].sum()

# Por cada item vendido: dias para vender= fecha venta - fecha compra
df_vendidos = df[df["fecha_venta"].notna()].copy()
df_vendidos["dias_para_vender"] = (df_vendidos["fecha_venta"] - df_vendidos["fecha_compra"]).dt.days
promedio_dias = df_vendidos["dias_para_vender"].mean()

color = "green" if total_beneficio >= 0 else "red"

show_ganancia=st.sidebar.title(f":{color}[Ganancia]")
show_ganancia=st.sidebar.subheader(
    f"**:{color}[{total_beneficio} CUP]**",
    divider="rainbow"
    )

# Si el df tiene datos: Generar los gráficos
if len(df) > 0:
    with st.sidebar:
        with st.sidebar:
            st.subheader("⏳ Tiempo promedio en vender un ítem")

            df_vendidos = df[df["fecha_venta"].notna()].copy()

            if len(df_vendidos) == 0:
                st.info("Todavía no hay ventas suficientes.")
            else:
                df_vendidos["dias_para_vender"] = (df_vendidos["fecha_venta"] - df_vendidos["fecha_compra"]).dt.days
                promedio_dias = df_vendidos["dias_para_vender"].mean()

                st.metric(
                    label="Promedio",
                    value=f"{promedio_dias:.1f} días"
                )
    # ====================================
    # Gráfico Productos Estancados
    # ====================================
    with st.container(border=True):
        st.subheader("Productos Estancados (más de 30 días sin vender)", divider="rainbow")

        df_stuck = df[df["stuck"] == True]

        if len(df_stuck) == 0:
            st.success("No tienes productos estancados. ¡Buen trabajo!")
        else:
            df_stuck["dias"] = df_stuck["dias_desde_compra"]

            fig_stuck = px.bar(
                df_stuck,
                x="item",
                y="dias",
                text="dias",
                color="dias",
                color_continuous_scale="Reds",
            )

            fig_stuck.update_layout(
                xaxis_title="Item",
                yaxis_title="Días sin vender",
                height=400
            )

            st.plotly_chart(fig_stuck, width="stretch")


    # ====================================
    # Gráfico Resumen General
    # ====================================
    with st.container(border=True):
        st.subheader("Resumen General", divider="rainbow")

        # Calcular ganancias de items vendidos individualmente
        ganancia_items_vendidos = df[df["fecha_venta"].notna()]["ganancia"].sum()

        resumen_df = pd.DataFrame({
            "Categoría": [
                "Total Gastado",
                "Inversión Actual",
                "Ingresos Totales",
                "Ganancia (Neta) en items vendidos",
                "Beneficio/Pérdida Total"
            ],
            "Cantidad (CUP)": [
                total_gastado,
                inversion_actual,
                total_vendido,
                ganancia_items_vendidos,
                total_beneficio
            ]
        })

        fig_resumen_bar = px.bar(
            resumen_df,
            x="Categoría",
            y="Cantidad (CUP)",
            text="Cantidad (CUP)"
        )

        fig_resumen_bar.update_traces(marker_color=["#e74c3c","#9b59b6", "#2ecc71", "#e67e22", "#3498db"])
        fig_resumen_bar.update_layout(height=450)
        fig_resumen_bar.update_traces(marker=dict(line=dict(color="white", width=1)))

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
        fig_mes.update_traces(marker=dict(line=dict(color="white", width=1)))

        st.subheader(":green[Ganancias] / :red[Pérdidas] Mensuales", divider="rainbow")
        st.plotly_chart(fig_mes, width="stretch")


    # -------------------------------------
    # Gráficos individuales
    # -------------------------------------
    with st.container(border=True):
        st.subheader(f"Ciclo de Ventas por Producto (Duración entre :red[Compra] y :green[Venta])", divider="rainbow")

        # --- PREPARAR DATAFRAME ---
        # Asegurar formato de fecha
        df["fecha_compra"] = pd.to_datetime(df["fecha_compra"])
        df["fecha_venta"] = pd.to_datetime(df["fecha_venta"], errors="coerce")

        # Duración en días
        df["dias"] = (df["fecha_venta"].fillna(pd.Timestamp.today()) - df["fecha_compra"]).dt.days

        # Beneficio solo para vendidos
        df["temp_ganancia"] = df["ganancia"].copy()
        df["temp_ganancia"] = df["fecha_venta"] - df["fecha_compra"]
        df.loc[df["fecha_venta"] == 0, "temp_ganancia"] = 0

        # Estado del item
        df["estado"] = df["fecha_venta"].apply(lambda x: "Vendido" if pd.notna(x) else "En inventario")

        # --- GRÁFICO GANTT ---
        fig_gantt = px.timeline(
            df,
            x_start="fecha_compra",
            x_end=df["fecha_venta"].fillna(pd.Timestamp.today()),
            y="item",
            color="estado",
            text="dias",
            hover_data={
                "fecha_compra": True,
                "fecha_venta": True,
                "precio_compra": True,
                "precio_venta": True,
                #"temp_ganancia": True,
                "dias": True,
                "estado": True,
                "ganancia": True
            },
            color_discrete_map={
                "Vendido": "#2ecc71",
                "En inventario": "#e74c3c",
            },
            labels={
                "x_end": "Fecha de Venta",
                "fecha_compra": "Fecha de Compra",
                "fecha_venta": "Fecha de Venta",
                "precio_compra": "Precio de Compra",
                "precio_venta": "Precio de Venta",
                "ganancia": "Ganancia",
                "dias": "Duración (días)",
                "estado": "Estado",
                "item": "Producto"
            }
        )

        fig_gantt.update_yaxes(autorange="reversed")  # estilo Gantt
        fig_gantt.update_traces(marker=dict(line=dict(color="white", width=1)))
        fig_gantt.update_layout(
            title="Historial de Compra/Venta",
            height=600,
            xaxis_title="Fecha",
            yaxis_title="Items",
        )

        st.plotly_chart(fig_gantt, width="stretch")

    with st.container(border=True):
        st.subheader("Gráficos por Ítem", divider="rainbow")

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
        fig_ganancia.update_traces(marker=dict(line=dict(color="white", width=1)))
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
        fig_cv.update_traces(marker=dict(line=dict(color="white", width=1)))
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

    with st.container(border=True):
        st.subheader("Desempeño por Categoría", divider="rainbow")

        df_cat = df.copy()

        # Convertir numéricos
        df_cat["precio_compra"] = pd.to_numeric(df_cat["precio_compra"], errors="coerce")
        df_cat["precio_venta"] = pd.to_numeric(df_cat["precio_venta"], errors="coerce")
        df_cat["ganancia"] = pd.to_numeric(df_cat["ganancia"], errors="coerce")

        # Filtrar solo vendidos para ganancia vendida
        df_vendidos = df_cat[df_cat["fecha_venta"].notna()].copy()
        df_vendidos["ganancia_vendida"] = df_vendidos["precio_venta"] - df_vendidos["precio_compra"]

        # Agrupación principal
        resumen_cat = df_cat.groupby("tipo").agg({
            "precio_compra": "sum",
            "precio_venta": "sum",
            "ganancia": "sum"
        }).reset_index()

        # Añadir columna de ganancia solo de vendidos
        ganancia_vendida_cat = df_vendidos.groupby("tipo")["ganancia_vendida"].sum().reset_index()
        resumen_cat = resumen_cat.merge(ganancia_vendida_cat, on="tipo", how="left")

        resumen_cat = resumen_cat.rename(columns={
            "precio_compra": "Total Compras",
            "precio_venta": "Total Ventas",
            "ganancia": "Ganancia Neta",
            "ganancia_vendida": "Ganancia Vendidos"
        })

        # Reemplazar NaN por 0 (categorías sin ventas)
        resumen_cat["Ganancia Vendidos"] = resumen_cat["Ganancia Vendidos"].fillna(0)

        # Grafico
        fig_cat = px.bar(
            resumen_cat.melt(id_vars="tipo", var_name="Tipo", value_name="CUP"),
            x="tipo",
            y="CUP",
            color="Tipo",
            barmode="group",
            color_discrete_map={
                "Total Compras": "#3498db",
                "Total Ventas": "#2ecc71",
                "Ganancia Neta": "#e74c3c",
                "Ganancia Vendidos": "#9b59b6"   # NUEVO color
            }
        )

        fig_cat.update_traces(marker=dict(line=dict(color="white", width=1)))
        st.plotly_chart(fig_cat, width="stretch")

    with st.container(border=True):
        st.subheader("Items Comprados y Vendidos por Categoría", divider="rainbow")

        # Cantidad comprada por categoría (todos los items)
        comprados = df["tipo"].value_counts().reset_index()
        comprados.columns = ["tipo", "comprados"]

        # Cantidad vendida por categoría (solo vendidos)
        vendidos = df[df["fecha_venta"].notna()]["tipo"].value_counts().reset_index()
        vendidos.columns = ["tipo", "vendidos"]

        # Unir ambos
        resumen = pd.merge(comprados, vendidos, on="tipo", how="left").fillna(0)

        # Convertir a formato largo para plotly
        resumen_melt = resumen.melt(
            id_vars="tipo",
            value_vars=["comprados", "vendidos"],
            var_name="Estado",
            value_name="Cantidad"
        )

        fig_count = px.bar(
            resumen_melt,
            x="tipo",
            y="Cantidad",
            color="Estado",                         # Color discreto → NO hay escala continua
            barmode="group",                        # Barras lado a lado
            text="Cantidad",
            color_discrete_map={
                "comprados": "#3498db",
                "vendidos": "#2ecc71",
            }
        )

        fig_count.update_traces(marker=dict(line=dict(color="white", width=1)))
        fig_count.update_layout(height=450)

        st.plotly_chart(fig_count, width="stretch")
    with st.container(border=True):
        st.subheader("Ganancia por Categoría", divider="rainbow")

        # Filtrar items vendidos
        df_vendidos = df[df["fecha_venta"].notna()].copy()

        # Asegurar conversión numérica
        df_vendidos["precio_compra"] = pd.to_numeric(df_vendidos["precio_compra"], errors="coerce")
        df_vendidos["precio_venta"] = pd.to_numeric(df_vendidos["precio_venta"], errors="coerce")

        # Calcular ganancia individual
        df_vendidos["ganancia"] = df_vendidos["precio_venta"] - df_vendidos["precio_compra"]

        # Filtrar solo ganancias positivas
        df_vendidos = df_vendidos[df_vendidos["ganancia"] > 0]

        if len(df_vendidos) == 0:
            st.info("Todavía no hay ganancias positivas para mostrar")
        else:
            # === Ganancias por categoría (suma total) ===
            cat_ganancias = (
                df_vendidos.groupby("tipo")["ganancia"]
                .sum()
                .reset_index()
                .rename(columns={"ganancia": "Ganancia"})
            )

            # === Selector de tipo de gráfico ===
            tipo_grafico = st.radio(
                "Tipo de gráfico",
                ["Barras", "Pie (%)"],
                horizontal=True
            )

            # === Modo barras ===
            if tipo_grafico == "Barras":
                fig_profit_bar = px.bar(
                    cat_ganancias,
                    x="tipo",
                    y="Ganancia",
                    text="Ganancia",
                    color="Ganancia",
                    color_continuous_scale="Viridis",
                    title="Ganancia por Categoría"
                )
                fig_profit_bar.update_traces(marker=dict(line=dict(color="white", width=1)))
                fig_profit_bar.update_layout(height=420)
                st.plotly_chart(fig_profit_bar, use_container_width=True)

            # === Modo Pie (%) ===
            else:
                fig_profit_pie = px.pie(
                    cat_ganancias,
                    names="tipo",
                    values="Ganancia",
                    hole=0.3,
                    title="Distribución porcentual de la ganancia por categoría"
                )
                fig_profit_pie.update_traces(textposition="inside", textinfo="percent+label")
                fig_profit_pie.update_traces(marker=dict(line=dict(color="white", width=1)))
                fig_profit_pie.update_layout(height=420)
                st.plotly_chart(fig_profit_pie, use_container_width=True)


else:
    st.info("Añade datos para ver los gráficos.")
