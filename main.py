import streamlit as st
import pandas as pd
import plotly.express as px
import openai

# Cargar los datos desde GitHub
url = 'https://raw.githubusercontent.com/99sarahi/Proyecto-Final/main/limpieza_proyecto.csv'
df = pd.read_csv(url, encoding='ISO-8859-1')

# Configurar el título del tablero
st.title("Dashboard Financiero Interactivo")

######################################### Filtros
# Filtros interactivos con opción "Todos"
# Estos filtros permiten al usuario seleccionar el sector, país y tamaño de la compañía
industry_options = ["Todos los sectores"] + list(df["Industry"].unique())
country_options = ["Todos los países"] + list(df["Country"].unique())
company_size_options = ["Todos los tamaños"] + list(df["Company_Size"].unique())

# Crear selecciones para los filtros
industry_filter = st.selectbox("Selecciona la Industria:", options=industry_options)
country_filter = st.selectbox("Selecciona el País:", options=country_options)
company_size_filter = st.selectbox("Selecciona el Tamaño de la Compañía:", options=company_size_options)

# Aplicar filtros según las selecciones del usuario, permitiendo "Todos"
filtered_df = df.copy()
if industry_filter != "Todos los sectores":
    filtered_df = filtered_df[filtered_df["Industry"] == industry_filter]
if country_filter != "Todos los países":
    filtered_df = filtered_df[filtered_df["Country"] == country_filter]
if company_size_filter != "Todos los tamaños":
    filtered_df = filtered_df[filtered_df["Company_Size"] == company_size_filter]

############################################## Gráficas de pastel
# Comentario sobre las gráficas de pastel
st.subheader("Distribución de Compañías")
st.caption("Las gráficas de pastel a continuación muestran la distribución de compañías según el país, industria y tamaño.")

#########################################
# Gráfico de pastel por País
country_count = filtered_df['Country'].value_counts().reset_index()
country_count.columns = ['Country', 'Count']
fig_country = px.pie(country_count, values='Count', names='Country')
fig_country.update_layout(
    legend=dict(y=1, orientation="h", yanchor="bottom", xanchor="center", x=0.5)  # Leyenda en la parte superior
)

# Encontrar el país con más compañías y su porcentaje
total_companies_country = country_count['Count'].sum()
max_country = country_count.loc[country_count['Count'].idxmax()]
max_country_name = max_country['Country']
max_country_count = max_country['Count']
max_country_percentage = (max_country_count / total_companies_country) * 100

# Comentario sobre el país con más compañías
st.write(f"El país con mayor cantidad de compañías es **{max_country_name}**, con un total de **{max_country_count}** empresas, representando el **{max_country_percentage:.2f}%** del total.")

#########################################
# Gráfico de pastel por Industria
industry_count = filtered_df['Industry'].value_counts().reset_index()
industry_count.columns = ['Industry', 'Count']
fig_industry = px.pie(industry_count, values='Count', names='Industry')
fig_industry.update_layout(
    legend=dict(y=1, orientation="h", yanchor="bottom", xanchor="center", x=0.5)  # Leyenda en la parte superior
)

# Encontrar la industria con más compañías y su porcentaje
total_companies_industry = industry_count['Count'].sum()
max_industry = industry_count.loc[industry_count['Count'].idxmax()]
max_industry_name = max_industry['Industry']
max_industry_count = max_industry['Count']
max_industry_percentage = (max_industry_count / total_companies_industry) * 100

# Comentario sobre la industria con más compañías
st.write(f"La industria con mayor cantidad de compañías es **{max_industry_name}**, con un total de **{max_industry_count}** empresas, representando el **{max_industry_percentage:.2f}%** del total.")

#########################################
# Gráfico de pastel por Tamaño de Compañía
company_size_count = filtered_df['Company_Size'].value_counts().reset_index()
company_size_count.columns = ['Company_Size', 'Count']
fig_company_size = px.pie(company_size_count, values='Count', names='Company_Size')
fig_company_size.update_layout(
    legend=dict(y=1, orientation="h", yanchor="bottom", xanchor="center", x=0.5)  # Leyenda en la parte superior
)

# Encontrar el tamaño de empresa con más compañías y su porcentaje
total_companies_size = company_size_count['Count'].sum()
max_size = company_size_count.loc[company_size_count['Count'].idxmax()]
max_size_name = max_size['Company_Size']
max_size_count = max_size['Count']
max_size_percentage = (max_size_count / total_companies_size) * 100

# Comentario sobre el tamaño de compañía con más empresas
st.write(f"El tamaño de compañía con mayor cantidad de empresas es **{max_size_name}**, con un total de **{max_size_count}** empresas, representando el **{max_size_percentage:.2f}%** del total.")

#########################################
# Mostrar gráficos

col1, col2 = st.columns(2)  # Dos columnas para las gráficas de arriba

# Gráfico de pastel por País
with col1:
    st.subheader("Compañías por País")
    fig_country.update_layout(width=400, height=400, margin=dict(l=20, r=20, t=20, b=20), showlegend=False)
    fig_country.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_country)

# Gráfico de pastel por Industria
with col2:
    st.subheader("Compañías por Industria")
    fig_industry.update_layout(width=400, height=400, margin=dict(l=20, r=20, t=20, b=20), showlegend=False)
    fig_industry.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_industry)

# Gráfico de pastel por Tamaño de Compañía
st.subheader("Compañías por Tamaño")
st.write("")  # Espacio vacío opcional
fig_company_size.update_layout(width=800, height=400, margin=dict(l=20, r=20, t=20, b=20), showlegend=False)
fig_company_size.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_company_size, use_container_width=True)

st.write('')
st.write('')


####################################### Top 5
# Mostrar el top 5 de compañías con mayor Total_Revenue dentro del DataFrame filtrado
st.subheader(f"Top 5 Compañías con Mayor Ingreso Total en {industry_filter}, {country_filter}, {company_size_filter}")
st.caption('Cifras en millones')

# Filtrar las top 5 compañías por Total_Revenue
top_5_companies = filtered_df.nlargest(5, 'Total_Revenue')[['Company_ID', 'Total_Revenue', "Industry", "Country", "Company_Size"]]

# Convertir Total_Revenue a millones de pesos
top_5_companies['Total_Revenue'] = (top_5_companies['Total_Revenue'] / 1_000_000).apply(lambda x: f"{x:,.2f}")

# Mostrar la tabla
st.table(top_5_companies)
st.write('')
st.write('')

#################################### Gráfico de Barras
st.subheader("Comparación del Ratio de Liquidez")
# Calcular la deuda a patrimonio promedio
average_cr = filtered_df['Current_Ratio'].mean()

# Mostrar el texto en el tablero con el valor calculado
st.write(f"El ratio de liquidez promedio es: **{average_cr:.2f}**")

liquidity_ratio_mean = filtered_df.groupby('Industry')['Current_Ratio'].mean().reset_index()
max_liquidity_industry = liquidity_ratio_mean.loc[liquidity_ratio_mean['Current_Ratio'].idxmax()]


fig_liquidity = px.bar(liquidity_ratio_mean, 
                        x='Industry', 
                        y='Current_Ratio', 
                        title='Ratio de Liquidez Promedio por Industria',
                        labels={'Current_Ratio': 'Ratio de Liquidez'},
                        text='Current_Ratio')

fig_liquidity.update_traces(texttemplate='%{text:.2f}', textposition='outside')
st.plotly_chart(fig_liquidity)

st.write(f"La industria con el ratio de liquidez promedio más alto es **{max_liquidity_industry['Industry']}**, con un ratio de **{max_liquidity_industry['Current_Ratio']:.2f}**.")
st.write('')


liquidity_ratio_mean = filtered_df.groupby('Country')['Current_Ratio'].mean().reset_index()
max_liquidity_industry = liquidity_ratio_mean.loc[liquidity_ratio_mean['Current_Ratio'].idxmax()]

fig_liquidity = px.bar(liquidity_ratio_mean, 
                        x='Country', 
                        y='Current_Ratio', 
                        title='Ratio de Liquidez Promedio por Pais',
                        labels={'Current_Ratio': 'Ratio de Liquidez'},
                        text='Current_Ratio')

fig_liquidity.update_traces(texttemplate='%{text:.2f}', textposition='outside')
st.plotly_chart(fig_liquidity)

st.write(f"El pais con el ratio de liquidez promedio más alto es **{max_liquidity_industry['Country']}**, con un ratio de **{max_liquidity_industry['Current_Ratio']:.2f}**.")
st.write('')



liquidity_ratio_mean = filtered_df.groupby('Company_Size')['Current_Ratio'].mean().reset_index()
max_liquidity_industry = liquidity_ratio_mean.loc[liquidity_ratio_mean['Current_Ratio'].idxmax()]

fig_liquidity = px.bar(liquidity_ratio_mean, 
                        x='Company_Size', 
                        y='Current_Ratio', 
                        title='Ratio de Liquidez Promedio por Pais',
                        labels={'Current_Ratio': 'Ratio de Liquidez'},
                        text='Current_Ratio')

fig_liquidity.update_traces(texttemplate='%{text:.2f}', textposition='outside')
st.plotly_chart(fig_liquidity)

st.write(f"El tamanio de empresa con el ratio de liquidez promedio más alto es **{max_liquidity_industry['Company_Size']}**, con un ratio de **{max_liquidity_industry['Current_Ratio']:.2f}**.")
st.write('')
st.write('')
st.write('')

############################################# Gráfica de barras del promedio de ingresos
st.subheader(f"Promedio de Ingresos (en millones) por Industria y Tamaño de Compañía para {country_filter}")

average_revenue = filtered_df.groupby(['Industry', 'Company_Size'])['Total_Revenue'].mean() / 1_000_000  # Dividir entre 1 millón
average_revenue = average_revenue.reset_index()

# Formatear los números con comas y dos decimales
average_revenue['Total_Revenue'] = average_revenue['Total_Revenue'].apply(lambda x: f"{x:,.2f}")

# Crear gráfico de barras
fig_revenue = px.bar(average_revenue, 
                      x='Industry', 
                      y='Total_Revenue', 
                      color='Company_Size', 
                      barmode='group',  # Cambiar a 'group' para columnas separadas
                      title='Promedio de Ingresos (en millones) por Industria y Tamaño de Compañía',
                      labels={'Total_Revenue': 'Promedio de Ingresos (en millones)', 'Company_Size': 'Tamaño de Compañía'},
                      text='Total_Revenue')

# Actualizar el formato del texto para mostrar separadores de miles y dos decimales
fig_revenue.update_traces(texttemplate='%{text}', textposition='outside')

# Mostrar gráfico
st.plotly_chart(fig_revenue)

st.write('')
st.write('')
st.write('')
#######################################################################################
# Calcular Deuda a Patrimonio
#filtered_df['Debt_to_Equity_Ratio'] = filtered_df['Total_Debt'] / filtered_df['Equity']
# Agregar la columna Total_Debt
filtered_df['Total_Debt'] = filtered_df['Short_Term_Debt'] + filtered_df['Long_Term_Debt']

# Convertir los montos a millones
debt_equity = filtered_df.groupby(['Industry', 'Company_Size'])[['Total_Debt', 'Equity']].sum().reset_index()
debt_equity['Total_Debt'] = debt_equity['Total_Debt'] / 1_000_000  # Convertir a millones
debt_equity['Equity'] = debt_equity['Equity'] / 1_000_000  # Convertir a millones

# Crear el gráfico de barras apiladas
fig_debt_equity = px.bar(debt_equity, 
                          x='Industry', 
                          y=['Total_Debt', 'Equity'], 
                          title='Proporción de Deuda a Patrimonio por Industria (en millones)',
                          labels={'value': 'Monto (Millones)', 'variable': 'Tipo'},
                          text_auto='.1f',  # Mostrar solo un decimal
                          barmode='stack')

# Actualizar el formato del texto para usar comas en miles y millones
fig_debt_equity.update_traces(
    #texttemplate='%{text:,.1f}M',  # Formato con comas y un decimal, agregando "M" para millones
    textposition='outside'
)

# Mostrar el gráfico
st.plotly_chart(fig_debt_equity)


# Gráfico de Barras
st.subheader("Cobertura de Gastos Financieros de las Principales Empresas")
financial_coverage_mean = filtered_df.groupby('Industry')['Interest_Coverage_Ratio'].mean().reset_index()

fig_financial_coverage = px.bar(financial_coverage_mean.nlargest(10, 'Interest_Coverage_Ratio'), 
                                  x='Industry', 
                                  y='Interest_Coverage_Ratio', 
                                  title='Cobertura de Gastos Financieros por Compañía (Top 10)',
                                  labels={'Interest_Coverage_Ratio': 'Cobertura de Gastos Financieros'},
                                  text='Interest_Coverage_Ratio')

fig_financial_coverage.update_traces(texttemplate='%{text:.2f}', textposition='outside')
st.plotly_chart(fig_financial_coverage)


###########################################################################################

# Sección de entrada de datos
st.subheader("Calculadora de Indicadores Financieros")

# Input de valores
current_assets = st.number_input("Activos Circulantes", min_value=0.0, value=0.0, step=0.1)
current_liabilities = st.number_input("Pasivos Circulantes", min_value=0.0, value=0.0, step=0.1)
total_debt = st.number_input("Deuda Total", min_value=0.0, value=0.0, step=0.1)
equity = st.number_input("Patrimonio Neto", min_value=0.0, value=0.0, step=0.1)
total_revenue = st.number_input("Ingresos Totales", min_value=0.0, value=0.0, step=0.1)
financial_expenses = st.number_input("Gastos Financieros", min_value=0.0, value=0.0, step=0.1)

# Selección de industria, país y tamaño de empresa
industry_input = st.selectbox("Selecciona la Industria", options=industry_options)
country_input = st.selectbox("Selecciona el País", options=country_options)
company_size_input = st.selectbox("Selecciona el Tamaño de la Empresa", options=company_size_options)

# Filtrar el DataFrame según los filtros seleccionados
filtered_df = df.copy()

if industry_input != "Todos los sectores":
    filtered_df = filtered_df[filtered_df["Industry"] == industry_input]
if country_input != "Todos los países":
    filtered_df = filtered_df[filtered_df["Country"] == country_input]
if company_size_input != "Todos los tamaños":
    filtered_df = filtered_df[filtered_df["Company_Size"] == company_size_input]

# Cálculos de ratios ingresados por el usuario
liquidity_ratio = current_assets / current_liabilities if current_liabilities != 0 else 0
debt_to_equity_ratio = total_debt / equity if equity != 0 else 0
interest_coverage_ratio = total_revenue / financial_expenses if financial_expenses != 0 else 0

# Cálculos de ratios promedio del DataFrame filtrado
avg_liquidity_ratio = filtered_df['Current_Ratio'].mean()
avg_debt_to_equity_ratio = filtered_df['Debt_to_Equity_Ratio'].mean()
avg_interest_coverage_ratio = filtered_df['Interest_Coverage_Ratio'].mean()

# Mostrar resultados y comparaciones

if liquidity_ratio > avg_liquidity_ratio:
    st.write(f"**El Ratio de Liquidez de su empresa es:** {liquidity_ratio:.2f} el cual está por encima del promedio general de otras empresas con condiciones demograficas similares a las suyas. **Promedio general: ({avg_liquidity_ratio:.2f})**.")
else:
    st.write(f"**El Ratio de Liquidez de tu empresa es:** {liquidity_ratio:.2f} el cual está por debajo del promedio general de otras empresas con condiciones demograficas similares a las suyas. **Promedio general:({avg_liquidity_ratio:.2f})**.")
    


if debt_to_equity_ratio > avg_debt_to_equity_ratio:
    st.write(f"**El Ratio de Deuda a Patrimonio de su empresa es:** {debt_to_equity_ratio:.2f} el cual está por encima del promedio general de otras empresas con condiciones demograficas similares a las suyas. **Promedio general: ({avg_debt_to_equity_ratio:.2f})**.")
else:
    st.write(f"**El Ratio de Deuda a Patrimonio de su empresa es:** {debt_to_equity_ratio:.2f} el cual está por debajo del promedio general de otras empresas con condiciones demograficas similares a las suyas. **Promedio general: ({avg_debt_to_equity_ratio:.2f})**.")



if interest_coverage_ratio > avg_interest_coverage_ratio:
    st.write(f"**La cobertura de gastos financieros de su empresa es:** {interest_coverage_ratio:.2f} el cual está por encima del promedio general de otras empresas con condiciones demograficas similares a las suyas. **Promedio general: ({avg_debt_to_equity_ratio:.2f})**")
else:
    st.write(f"**La cobertura de gastos financieros de su empresa es:** {interest_coverage_ratio:.2f} el cual está por debajo del promedio general de otras empresas con condiciones demograficas similares a las suyas. **Promedio general: ({avg_debt_to_equity_ratio:.2f})**")


# Instanciar el cliente de OpenAI
client = openai.OpenAI(api_key=openai_api_key)


def obtener_respuesta(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Ajusta el modelo según lo que necesites
        messages=[
            {"role": "system", "content": """
            Eres un financiero que trabaja analizando y comparando los indicadores de solvencia de distintas empresas, eres experto en el área de solvencia,
            entonces vas a responder todo desde la perspectiva de un financiero. Contesta siempre en español
            en un máximo de 50 palabras.
            """}, #Solo podemos personalizar la parte de content
            {"role": "user", "content": prompt}
        ]
    )
    output = response.choices[0].message.content
    return output

prompt_user = st.text_area("Ingresa tu pregunta:")

output = obtener_respuesta(prompt_user)
