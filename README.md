# Dashboard de Compras y Ventas

Un dashboard interactivo desarrollado con Streamlit para gestionar y visualizar tus compras y ventas de productos. Permite llevar un registro detallado de tus transacciones, calcular ganancias/pérdidas y visualizar los datos mediante gráficos interactivos.

## Características

- **Gestión de ítems**: Añade nuevos productos con información de compra y venta
- **Tabla editable**: Modifica los datos directamente desde la interfaz
- **Cálculo automático**: Calcula automáticamente las ganancias/pérdidas por ítem
- **Visualizaciones interactivas**:
  - Gráfico de resumen general (Gastado, Ingresos, Beneficio)
  - Gráfico de ganancias/pérdidas por ítem (con colores verde/rojo)
  - Comparación de precios de compra vs venta
- **Persistencia de datos**: Los datos se guardan en un archivo CSV local
- **Ordenamiento**: Ordena la tabla por fecha de compra

## Tecnologías Utilizadas

- **Streamlit**: Framework para crear aplicaciones web interactivas
- **Pandas**: Manipulación y análisis de datos
- **Plotly**: Gráficos interactivos
- **NumPy**: Operaciones numéricas

## Requisitos

- Python >= 3.11
- Las dependencias se encuentran en `requirements.txt`

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/dashboard_sales.git
cd dashboard_sales
```

2. Crea un entorno virtual (recomendado):
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Cómo usar?

1. Ejecuta la aplicación:
```bash
streamlit run dashboard.py
```

2. Abre tu navegador en la URL que aparece en la terminal (generalmente `http://localhost:8501`)

3. **Añadir un nuevo ítem**:
   - Completa el formulario con el nombre del ítem, precio de compra y fecha de compra
   - Opcionalmente, añade el precio y fecha de venta si ya lo has vendido
   - Haz clic en "Añadir"

4. **Editar datos**:
   - Modifica los datos directamente en la tabla
   - Haz clic en "Guardar tabla" para persistir los cambios

5. **Visualizar gráficos**:
   - Los gráficos se actualizan automáticamente según los datos ingresados

## Estructura del Proyecto

```
dashboard_sales/
├── dashboard.py          # Aplicación principal de Streamlit
├── data.csv              # Archivo CSV con los datos (se crea automáticamente)
├── requirements.txt      # Dependencias del proyecto
└── README.md            # Este archivo
```

## Formato de Datos

El archivo `data.csv` contiene las siguientes columnas:
- `item`: Nombre del producto
- `fecha_compra`: Fecha de compra (formato: YYYY-MM-DD)
- `precio_compra`: Precio de compra
- `fecha_venta`: Fecha de venta (opcional, formato: YYYY-MM-DD)
- `precio_venta`: Precio de venta (opcional)
- `ganancia`: Ganancia calculada automáticamente (precio_venta - precio_compra)

## Contribuciones

Las contribuciones son bienvenidas. Si tienes sugerencias o encuentras algún problema, por favor abre un issue o envía un pull request. Este proyecto fue creado para uso personal principalmente porque necesitaba algo simple y rápido para controlar las finanzas de un negocio

---

Desarrollado usando Streamlit para mayor facilidad

