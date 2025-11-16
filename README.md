
---

# Dashboard de Compras y Ventas

Un dashboard interactivo desarrollado con **Streamlit** para gestionar y visualizar compras y ventas de productos.
Permite llevar un registro detallado de transacciones, calcular ganancias/pérdidas y generar gráficos interactivos en tiempo real.

---

## Características

### ✔ Gestión de ítems

* Añadir nuevos productos con fecha y precio de compra/venta.
* Cálculo automático de ganancia/pérdida.

### ✔ Tabla editable

* Edita directamente en la interfaz.
* Cambios reflejados al instante.

### ✔ Visualizaciones

* **Resumen General** (Gastado, Ingresos y Beneficio total).
* **Ganancia/Pérdida por ítem** (colores verde/rojo).
* **Precio Compra vs Precio Venta** con líneas comparativas.

### ✔ Persistencia de datos

* Usa un archivo `data.csv` editable, exportable y recargable.

### ✔ Ordenamiento

* Orden por fecha de compra con un clic.

### ✔ Ejecución local rápida

* Incluye un launcher local:

  **`run_dashboard.command`** (macOS)
  que abre la app con doble clic usando el entorno virtual.

---

## Tecnologías Utilizadas

* **Streamlit** – Interfaz interactiva
* **Pandas** – Manipulación de datos
* **Plotly** – Gráficos dinámicos
* **NumPy** – Cálculos adicionales

---

## Requisitos

* **Python 3.11 o superior**
* Dependencias listadas en `requirements.txt`

Si usas el archivo **run_dashboard.command**, el entorno virtual se encarga del resto.

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/dashboard_sales.git
cd dashboard_sales
```

---

### 2. Crear un entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate    # En Windows: venv\Scripts\activate
```

---

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecución

### ✔ Opción A: Usar el launcher local (macOS) — Recomendado

Haz doble clic en:

```
run_dashboard.command
```

Este archivo:

* activa automáticamente el entorno virtual,
* ejecuta Streamlit,
* y abre la app en tu navegador.

---

### ✔ Opción B: Ejecutar manualmente con Python

```bash
python3 -m streamlit run dashboard.py
```

Luego abre en tu navegador:

```
http://localhost:8501
```

---

## Cómo usar

### Añadir ítems

1. Ingresa nombre del producto, fecha y precio.
2. (Opcional) Agrega precio y fecha de venta.
3. Presiona **“Añadir”**.

La ganancia se calcula automáticamente.

---

### Editar datos

* Edita cualquier celda desde la tabla interactiva.
* Los cambios se guardan en el estado interno.

---

### Ver gráficos

* Se generan automáticamente:

  * Resumen general
  * Ganancia/Pérdida por producto
  * Comparación precio compra vs venta

---

## Estructura del Proyecto

```
dashboard_sales/
├── dashboard.py             # Aplicación principal
├── data.csv                 # Datos (se crea automáticamente)
├── run_dashboard.command    # Launcher para macOS
├── requirements.txt         # Dependencias
└── README.md                # Este archivo
```

---

## Formato del archivo data.csv

| COLUMNA       | DESCRIPCIÓN                  |
| ------------- | ---------------------------- |
| item          | Nombre del producto          |
| fecha_compra  | Fecha de compra (YYYY-MM-DD) |
| precio_compra | Precio de compra             |
| fecha_venta   | Fecha de venta (opcional)    |
| precio_venta  | Precio de venta (opcional)   |
| ganancia      | precio_venta - precio_compra |

---

## 🆕 Últimos cambios

* Eliminado sistema .exe / .app (no necesario en macOS).
* Añadido **run_dashboard.command** para ejecución rápida.
* Captura correcta del entorno virtual para evitar errores al ejecutar.
* Mejoras en la tabla editable y manejo de fechas.
* Ajustes visuales en gráficos.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas.
Puedes abrir **issues** o **pull requests** con mejoras o sugerencias.

---

## 🧑‍💻 Desarrollado con Streamlit

Sencillo, rápido y extensible.

---

Si quieres, también te preparo una versión del README con iconos, emojis o estilo más formal/profesional.
