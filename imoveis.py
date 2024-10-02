import streamlit as st
import pandas as pd
import plotly.express as px

# Configurando a página para usar o layout completo
st.set_page_config(layout="wide")

# Lendo o arquivo CSV
df = pd.read_csv("houses_to_rent_v2.csv", sep=';')

# Convertendo a coluna 'total (R$)' para numérica, se necessário
df['total (R$)'] = pd.to_numeric(df['total (R$)'], errors='coerce')

# Exibindo o título do aplicativo
st.title("Análise de Imóveis para Aluguel")

# Adicionando um filtro de cidade na barra lateral
cidades = df['city'].unique()  # Obtendo as cidades únicas do dataset
cidade_selecionada = st.sidebar.selectbox("Selecione a cidade", ["Todas"] + list(cidades))

# Adicionando filtro se aceita animal ou não na barra lateral
aceita_animal = st.sidebar.selectbox("Aceita Animais?", ["Todos", "Sim", "Não"])

# Adicionando filtro se tem mobília ou não na barra lateral
tem_mobilia = st.sidebar.selectbox("Tem Mobília?", ["Todos", "Sim", "Não"])

# Adicionando filtro de valor inicial e final da coluna 'total (R$)'
min_valor, max_valor = st.sidebar.slider(
    "Selecione o intervalo de valor total (R$)", 
    float(df['total (R$)'].min()), 
    float(df['total (R$)'].max()), 
    (float(df['total (R$)'].min()), float(df['total (R$)'].max()))
)

# Aplicando os filtros
df_filtrado = df.copy()

# Filtrando por cidade (caso não seja "Todas")
if cidade_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado['city'] == cidade_selecionada]

# Filtrando se aceita animais
if aceita_animal != "Todos":
    df_filtrado = df_filtrado[df_filtrado['animal'] == aceita_animal]

# Filtrando se tem mobília
if tem_mobilia != "Todos":
    df_filtrado = df_filtrado[df_filtrado['furniture'] == tem_mobilia]

# Filtrando por valor total (R$) dentro do intervalo escolhido
df_filtrado = df_filtrado[(df_filtrado['total (R$)'] >= min_valor) & (df_filtrado['total (R$)'] <= max_valor)]

# Exibindo a quantidade de imóveis disponíveis após os filtros
st.subheader(f"Imóveis disponíveis após filtros: {len(df_filtrado)}")

# Contando a quantidade de imóveis por cidade no DataFrame filtrado
df_cidades_agrupadas = df_filtrado.groupby('city').size().reset_index(name='Quantidade de Imóveis')

# Gráfico de barras exibindo todas as cidades e a quantidade de imóveis, com cores customizadas e rótulos
fig_cidade = px.bar(df_cidades_agrupadas, x='city', y='Quantidade de Imóveis', 
                    title='Número de Imóveis Disponíveis por Cidade', 
                    labels={'Quantidade de Imóveis': 'Quantidade de Imóveis', 'city': 'Cidade'}, 
                    height=400, text_auto=True,
                    color_discrete_sequence=['#6A5ACD'])

# Ajustando o layout para remover linhas e contornos indesejados
fig_cidade.update_layout(
    xaxis=dict(showline=False, showgrid=False),
    yaxis=dict(showline=False, showgrid=False),
    plot_bgcolor='rgba(0,0,0,0)'  # Remove fundo do gráfico
)

# Exibindo o gráfico de barras com rótulos de quantidade de imóveis por cidade
st.plotly_chart(fig_cidade, use_container_width=True)

# Criando colunas lado a lado para os gráficos de pizza
col1, col2 = st.columns(2)

# Gráfico 2: Aceitação de animais (atualizado após filtro) em formato de pizza com quantidade em vez de porcentagem
with col1:
    if not df_filtrado.empty:  # Evitar gráfico vazio
        df_animais_agrupados = df_filtrado.groupby('animal').size().reset_index(name='Quantidade de Imóveis')
        fig_animais = px.pie(df_animais_agrupados, names='animal', values='Quantidade de Imóveis',
                             title="Aceitação de Animais nos Imóveis Filtrados",
                             labels={'animal': 'Aceita Animais'}, height=400,
                             color_discrete_sequence=['#6A5ACD', '#B0C4DE'])
        # Adicionando rótulos com a quantidade de imóveis
        fig_animais.update_traces(textinfo='label+value')
        st.plotly_chart(fig_animais, use_container_width=True)
    else:
        st.write("Nenhum imóvel encontrado para o filtro aplicado.")

# Gráfico 3: Presença de mobília (atualizado após filtro) em formato de pizza com quantidade em vez de porcentagem
with col2:
    if not df_filtrado.empty:  # Evitar gráfico vazio
        df_mobilia_agrupados = df_filtrado.groupby('furniture').size().reset_index(name='Quantidade de Imóveis')
        fig_mobilia = px.pie(df_mobilia_agrupados, names='furniture', values='Quantidade de Imóveis',
                             title="Presença de Mobília nos Imóveis Filtrados",
                             labels={'furniture': 'Mobília'}, height=400,
                             color_discrete_sequence=['#6A5ACD', '#B0C4DE'])
        # Adicionando rótulos com a quantidade de imóveis
        fig_mobilia.update_traces(textinfo='label+value')
        st.plotly_chart(fig_mobilia, use_container_width=True)
    else:
        st.write("Nenhum imóvel encontrado para o filtro aplicado.")

# Gráfico de barras horizontal da coluna 'area'
if not df_filtrado.empty:  # Evitar gráfico vazio
    fig_area = px.bar(df_filtrado, x='area', y='city', 
                      title='Distribuição de Área por Cidade',
                      labels={'area': 'Área (m²)', 'city': 'Cidade'}, 
                      orientation='h', height=400, 
                      color_discrete_sequence=['#6A5ACD'])

    # Ajustando o layout para remover contornos indesejados
    fig_area.update_layout(
        xaxis=dict(showline=False, showgrid=False),
        yaxis=dict(showline=False, showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)'  # Remove fundo do gráfico
    )

    # Exibindo o gráfico de barras horizontal
    st.plotly_chart(fig_area, use_container_width=True)
else:
    st.write("Nenhum dado disponível para o gráfico de área.")
