import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Dashboard de Compras/Ventas", layout="wide")

DATA_FILE = "data.csv"

# ------------------------------------
# Cargar o crear dataset inicial
# ------------------------------------
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=[
        "item", "fecha_compra", "precio_compra", "fecha_venta", "precio_venta", "ganancia"
    ])
    df.to_csv(DATA_FILE, index=False)

st.title("Dashboard de Compras y Ventas")

# ------------------------------------
# Formulario de nuevo ítem
# ------------------------------------
st.subheader("Añadir nuevo ítem")

st.subheader("Añadir nuevo ítem")

col1, col2 = st.columns(2)

# Inputs dinámicos
item = col1.text_input("Item")
precio_compra = col1.number_input("Precio de compra", min_value=0.0, value=0.0)
fecha_compra = col1.date_input("Fecha de compra")

precio_venta = col2.number_input("Precio de venta (opcional)", min_value=0.0, value=0.0)
fecha_venta = col2.date_input("Fecha de venta (opcional)", value=None)

# ✔ Ganancia dinámica
ganancia = precio_venta - precio_compra if precio_venta > 0 else 0
col2.number_input("Ganancia", value=ganancia)

# Botón de añadir
if st.button("Añadir"):
    new_row = {
        "item": item,
        "fecha_compra": str(fecha_compra),
        "precio_compra": precio_compra,
        "precio_venta": precio_venta if precio_venta > 0 else "",
        "fecha_venta": str(fecha_venta) if precio_venta > 0 else "",
        "ganancia": ganancia if precio_venta > 0 else 0
    }

    df.loc[len(df)] = new_row
    df.to_csv(DATA_FILE, index=False)
    st.success("Ítem añadido correctamente")

# ------------------------------------
# Tabla editable
# ------------------------------------
st.subheader("Tabla de datos")

# Convertir fechas
df["fecha_compra"] = pd.to_datetime(df["fecha_compra"], errors="coerce")
df["fecha_venta"] = pd.to_datetime(df["fecha_venta"], errors="coerce")

# Botón ordenar
if st.button("Ordenar tabla por fecha de compra"):
    df = df.sort_values("fecha_compra", ascending=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("Tabla ordenada por fecha de compra")

# Editor
edited_df = st.data_editor(df, num_rows="dynamic")

if st.button("Guardar tabla"):
    edited_df.to_csv(DATA_FILE, index=False)
    st.success("Datos guardados")



# ------------------------------------
# Totales para gráfico resumen
# ------------------------------------
total_gastado = df["precio_compra"].sum()
total_vendido = df["precio_venta"].replace("", 0).astype(float).sum()
total_beneficio = df["ganancia"].astype(float).sum()


# ------------------------------------
# Gráfico grande resumen
# ------------------------------------
st.subheader("Resumen general")

resumen_df = pd.DataFrame({
    "Categoria": ["Gastado", "Ingresos por ventas", "Beneficio total"],
    "Cantidad": [total_gastado, total_vendido, total_beneficio]
})

fig_resumen = px.bar(
    resumen_df,
    x="Categoria",
    y="Cantidad",
    text="Cantidad"
)

fig_resumen.update_traces(marker_color=["#e74c3c", "#3498db", "#2ecc71"])
fig_resumen.update_layout(height=450)

st.plotly_chart(fig_resumen, use_container_width=True)


# ------------------------------------
# Gráficos individuales
# ------------------------------------
st.subheader("Gráficos por Item")

colg1, colg2 = st.columns(2)

# Gráfico de ganancias con colores (verde y rojo)
if len(df) > 0:
    df["ganancia_color"] = df["ganancia"].astype(float).apply(
        lambda x: "green" if x > 0 else "red"
    )

    fig_ganancia = px.bar(
        df,
        x="item",
        y="ganancia",
        color="ganancia_color",
        color_discrete_map={"green": "green", "red": "red"},
        title="Ganancia / Pérdida por Item",
        category_orders={"item": df["item"].tolist()} # para que mantengan el orden de la tabla
    )
    
    colg1.plotly_chart(fig_ganancia, use_container_width=True)

    # Compra vs venta
    fig_cv = px.line(
        df,
        x="item",
        y=["precio_compra", "precio_venta"],
        title="Precio Compra vs Venta",
        color_discrete_map={"precio_compra": "green", "precio_venta": "red"}
    )
    
    colg2.plotly_chart(fig_cv, use_container_width=True)

else:
    st.info("Añade datos para ver los gráficos.")
