# Proyecto-Final
# Dashboard Financiero Interactivo

Este proyecto es un **Dashboard Financiero Interactivo** construido en Python utilizando **Streamlit** y **Plotly**. El objetivo de este dashboard es visualizar y analizar indicadores financieros clave de diversas empresas, permitiendo a los usuarios interactuar con los datos a través de filtros y gráficos dinámicos.

## Funcionalidades

1. **Cargar datos financieros:**
   - Los datos son cargados desde un archivo CSV en GitHub que contiene información financiera sobre compañías de diversos sectores, países y tamaños.

2. **Filtros interactivos:**
   - Los usuarios pueden filtrar los datos por industria, país y tamaño de la empresa para obtener análisis más específicos.

3. **Gráficas de pastel:**
   - Se visualiza la distribución de empresas por país, industria y tamaño mediante gráficos de pastel (pie charts).

4. **Top 5 de compañías con mayores ingresos:**
   - Se muestra una tabla con las 5 compañías que tienen mayores ingresos, basados en los filtros seleccionados.

5. **Visualización de ratios financieros:**
   - Se generan gráficos de barras que muestran el *Current Ratio* (liquidez corriente), el *Debt-to-Equity Ratio* (Deuda a Patrimonio), y la *Interest Coverage Ratio* (Cobertura de Gastos Financieros) por industria, país y tamaño de la compañía.

6. **Comparación personalizada de ratios financieros:**
   - Los usuarios pueden ingresar sus propios datos financieros y comparar ratios como el *Current Ratio*, *Debt-to-Equity Ratio* y *Interest Coverage Ratio* con el promedio de las empresas en los filtros seleccionados.

7. **Chat financiero con OpenAI:**
   - Los usuarios pueden hacer preguntas sobre los indicadores financieros y recibir respuestas generadas por OpenAI en español.

## Requisitos

- Python 3.8+
- Paquetes necesarios:
  - Streamlit
  - Pandas
  - Plotly
  - OpenAI

