
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

* Incluye launchers locales para diferentes sistemas operativos:

  **Windows:** `launch_app.bat` - Ejecuta la app con doble clic
  **macOS:** `run_dashboard.command` - Ejecuta la app con doble clic (cambia el path en el archivo para seleccionar el tuyo propio)

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

**Windows:** Si usas el archivo **install.bat**, la instalación se realiza automáticamente.  
**macOS:** Si usas el archivo **run_dashboard.command**, el entorno virtual se encarga del resto.

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/dashboard_sales.git
cd dashboard_sales
```

---

### 2. Instalación en Windows — Recomendado

**Opción A: Instalación automática (más fácil)**

Haz doble clic en:

```
install.bat
```

Este archivo:

* Verifica que Python esté instalado
* Instala automáticamente todas las dependencias necesarias
* Configura el entorno para ejecutar la aplicación

**Opción B: Instalación manual**

```bash
# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

---

### 3. Instalación en macOS/Linux

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## Ejecución

### ✔ Windows — Opción A: Launcher automático (Recomendado)

Haz doble clic en:

```
launch_app.bat
```

Este archivo:

* Verifica que los archivos necesarios estén presentes
* Ejecuta Streamlit automáticamente
* Abre la app en tu navegador en `http://localhost:8501`

**Nota:** Para cerrar la aplicación, presiona `Ctrl+C` en la ventana de comandos.

---

### ✔ Windows — Opción B: Modo Administrador (Solución de problemas)

Si tienes problemas con la ejecución normal, haz doble clic en:

```
admin_setings.bat
```

Este archivo:

* Limpia el puerto 8501 si está ocupado
* Verifica que todos los archivos estén presentes
* Reinstala dependencias si faltan
* Inicia la aplicación con permisos elevados

---

### ✔ macOS — Opción A: Launcher automático (Recomendado)

Haz doble clic en:

```
run_dashboard.command
```

Este archivo:

* Activa automáticamente el entorno virtual
* Ejecuta Streamlit
* Abre la app en tu navegador

**Nota:** Puede que necesites cambiar el path del entorno virtual en el archivo según tu configuración.

---

### ✔ Opción C: Ejecutar manualmente con Python

**Windows:**
```bash
streamlit run dashboard.py
```

**macOS/Linux:**
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
├── install.bat              # Instalador automático para Windows
├── launch_app.bat           # Launcher para Windows
├── admin_setings.bat        # Modo administrador/solución de problemas (Windows)
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

### Windows
* ✅ Añadido **install.bat** - Instalador automático que verifica Python e instala dependencias
* ✅ Añadido **launch_app.bat** - Launcher con verificación de archivos y ejecución automática
* ✅ Añadido **admin_setings.bat** - Modo administrador para solución de problemas (libera puerto, reinstala dependencias)
* ✅ Soporte completo para Windows con scripts batch optimizados
* ✅ Interfaz de consola mejorada con caracteres UTF-8

### General
* ✅ Mejoras en la tabla editable y manejo de fechas
* ✅ Ajustes visuales en gráficos
* ✅ Mejor manejo de errores y mensajes informativos

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas.
Puedes abrir **issues** o **pull requests** con mejoras o sugerencias.

---

## 🧑‍💻 Desarrollado con Streamlit

Sencillo, rápido y extensible.

---

Si quieres, también te preparo una versión del README con iconos, emojis o estilo más formal/profesional.
