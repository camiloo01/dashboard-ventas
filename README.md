# 📊 Dashboard de Ventas — Comparativa Anual

App web construida con **Streamlit + Plotly + Pandas** para comparar ventas año vs año con filtros dinámicos encadenados.

---

## 📁 Estructura del Proyecto

```
dashboard_ventas/
│
├── app.py                        # Entry point principal
├── requirements.txt              # Dependencias
│
└── src/
    ├── components/               # Componentes visuales (UI)
    │   ├── charts.py             # Gráficos (línea, barras, crecimiento)
    │   ├── export.py             # Botón de descarga CSV
    │   ├── kpis.py               # Tarjetas de indicadores clave
    │   └── table.py              # Tabla detallada por Fabricante
    │
    └── utils/                    # Lógica y utilidades
        ├── config.py             # Configuración de página y estilos CSS
        ├── data_loader.py        # Carga, limpieza y parseo de archivos
        ├── filters.py            # Sidebar y aplicación de filtros
        └── helpers.py            # Formato de números y cálculos
```

---

## 🚀 Correr localmente

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar
streamlit run app.py
```

La app abre en: http://localhost:8501

---

## ☁️ Desplegar en Streamlit Cloud (gratis)

1. Sube esta carpeta a un repositorio de **GitHub**
2. Ve a https://share.streamlit.io
3. Conecta tu repo y selecciona `app.py` como entry point
4. Haz clic en **Deploy** — en 2-3 minutos tendrás un link público

---

## 📋 Columnas requeridas en el Excel

| Columna              | Descripción                  |
|----------------------|------------------------------|
| `Fecha_doc`          | Fecha de la venta (dd/mm/yyyy) |
| `Ingreso`            | Valor de la venta en COP     |
| `Cantidad`           | Unidades vendidas            |
| `Fabricante`         | Marca del producto           |
| `Region`             | Región de la venta           |
| `Descripción Centro` | Nombre de la tienda / CAV    |
| `Gama`               | Segmento del producto        |
| `Canal`              | Canal de venta               |

---

## ✨ Funcionalidades

- 📂 Carga de 2 archivos Excel (año anterior vs actual)
- 🔍 Filtros encadenados: Región → Tienda → Fabricante → Gama → Canal
- 📅 Vista Mensual / Semanal / Diaria
- 📈 KPIs con % de variación
- 📊 Gráficos comparativos interactivos
- 📋 Tabla detallada por fabricante
- ⬇️ Exportación a CSV
