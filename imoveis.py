# Bibliotecas Usadas

import streamlit as st
import pandas as pd
import plotly.express as px

# Documentação da Biblioteca plotly https://dash.plotly.com/
# Documentação da Biblioteca streamlit https://docs.streamlit.io/
# Correção de sintaxe com o chatgpt

# Configurando a página para usar o layout completo (Função do Streamlit)
st.set_page_config(layout="wide")

# Lendo o arquivo CSV
df = pd.read_csv("houses_to_rent_v2.csv", sep=';')

# Convertendo a coluna 'rent amount (R$)' para numérica, se necessário
df['rent amount (R$)'] = pd.to_numeric(df['rent amount (R$)'], errors='coerce')

# Exibindo o título do aplicativo
st.title("Análise de Imóveis para Aluguel")

# Adicionando filtros dinâmicos na barra lateral
st.sidebar.header("Filtros")

# Filtro de cidade
cidades = df['city'].unique()  # Obtendo as cidades únicas do dataset
cidade_selecionada = st.sidebar.selectbox("Selecione a cidade", ["Todas"] + list(cidades))

# Filtro se aceita animal ou não
aceita_animal = st.sidebar.selectbox("Aceita Animais?", ["Todos", "Sim", "Não"])

# Filtro se tem mobília ou não
tem_mobilia = st.sidebar.selectbox("Tem Mobília?", ["Todos", "Sim", "Não"])

# Filtro de valor de aluguel
min_valor, max_valor = st.sidebar.slider(
    "Selecione o intervalo de valor do aluguel (R$)", 
    float(df['rent amount (R$)'].min()), 
    float(df['rent amount (R$)'].max()), 
    (float(df['rent amount (R$)'].min()), float(df['rent amount (R$)'].max()))
)

# Filtro para quantidade de quartos
num_quartos = st.sidebar.slider(
    "Número de quartos", 
    int(df['rooms'].min()), 
    int(df['rooms'].max()), 
    (int(df['rooms'].min()), int(df['rooms'].max()))
)

# Filtro para quantidade de banheiros
num_banheiros = st.sidebar.slider(
    "Número de banheiros", 
    int(df['bathroom'].min()), 
    int(df['bathroom'].max()), 
    (int(df['bathroom'].min()), int(df['bathroom'].max()))
)

# Aplicando os filtros
df_filtrado = df.copy()

# Filtrando por cidade
if cidade_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado['city'] == cidade_selecionada]

# Filtrando se aceita animais
if aceita_animal != "Todos":
    df_filtrado = df_filtrado[df_filtrado['animal'] == aceita_animal]

# Filtrando se tem mobília
if tem_mobilia != "Todos":
    df_filtrado = df_filtrado[df_filtrado['furniture'] == tem_mobilia]

# Filtrando por valor do aluguel dentro do intervalo selecionado
df_filtrado = df_filtrado[(df_filtrado['rent amount (R$)'] >= min_valor) & (df_filtrado['rent amount (R$)'] <= max_valor)]

# Filtrando por número de quartos
df_filtrado = df_filtrado[(df_filtrado['rooms'] >= num_quartos[0]) & (df_filtrado['rooms'] <= num_quartos[1])]

# Filtrando por número de banheiros
df_filtrado = df_filtrado[(df_filtrado['bathroom'] >= num_banheiros[0]) & (df_filtrado['bathroom'] <= num_banheiros[1])]

# Exibindo a quantidade de imóveis disponíveis após os filtros
st.subheader(f"Imóveis disponíveis: {len(df_filtrado)}")

# Gráfico 1: Quantidade de imóveis por cidade
if not df_filtrado.empty:
    df_cidades_agrupadas = df_filtrado.groupby('city').size().reset_index(name='Quantidade de Imóveis')
    fig_cidade = px.bar(df_cidades_agrupadas, x='city', y='Quantidade de Imóveis', 
                        title='Número de Imóveis Disponíveis por Cidade', 
                        labels={'Quantidade de Imóveis': 'Quantidade de Imóveis', 'city': 'Cidade'}, 
                        height=400, text_auto=True,
                        color_discrete_sequence=['#6A5ACD'])

    fig_cidade.update_layout(
        xaxis=dict(showline=False, showgrid=False),
        yaxis=dict(showline=False, showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)'  # Remove fundo do gráfico
    )

    st.plotly_chart(fig_cidade, use_container_width=True)
else:
    st.write("Nenhum imóvel disponível para os filtros aplicados.")

# Criando colunas lado a lado para os gráficos de pizza
col1, col2 = st.columns(2)

# Gráfico 2: Aceitação de animais
with col1:
    if not df_filtrado.empty:  
        df_animais_agrupados = df_filtrado.groupby('animal').size().reset_index(name='Quantidade de Imóveis')
        fig_animais = px.pie(df_animais_agrupados, names='animal', values='Quantidade de Imóveis',
                             title="Aceitação de Animais nos Imóveis Filtrados",
                             labels={'animal': 'Aceita Animais'}, height=400,
                             color_discrete_sequence=['#6A5ACD', '#B0C4DE'])

        fig_animais.update_traces(textinfo='value')
        st.plotly_chart(fig_animais, use_container_width=True)
    else:
        st.write("Nenhum imóvel encontrado para o filtro aplicado.")

# Gráfico 3: Presença de mobília
# Site utilizado para escolha das cores https://erikasarti.com/html/tabela-cores/
with col2:
    if not df_filtrado.empty:  
        df_mobilia_agrupados = df_filtrado.groupby('furniture').size().reset_index(name='Quantidade de Imóveis')
        fig_mobilia = px.pie(df_mobilia_agrupados, names='furniture', values='Quantidade de Imóveis',
                             title="Presença de Mobília nos Imóveis Filtrados",
                             labels={'furniture': 'Mobília'}, height=400,
                             color_discrete_sequence=['#6A5ACD', '#B0C4DE'])

        fig_mobilia.update_traces(textinfo='value')
        st.plotly_chart(fig_mobilia, use_container_width=True)
    else:
        st.write("Nenhum imóvel encontrado para o filtro aplicado.")

# Gráfico 4: Distribuição da área por cidade
if not df_filtrado.empty:  
    fig_area = px.bar(df_filtrado, x='area', y='city', 
                      title='Distribuição de Área por Cidade',
                      labels={'area': 'Área (m²)', 'city': 'Cidade'}, 
                      orientation='h', height=400, 
                      color_discrete_sequence=['#6A5ACD'])

    fig_area.update_layout(
        xaxis=dict(showline=False, showgrid=False),
        yaxis=dict(showline=False, showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)'  
    )

    st.plotly_chart(fig_area, use_container_width=True)
else:
    st.write("Nenhum dado disponível para o gráfico de área.")

# Gráfico 5: Comparativo de Valores de Aluguel por Cidade
if not df_filtrado.empty:
    df_rent_avg = df_filtrado.groupby('city')['rent amount (R$)'].mean().reset_index()
    fig_rent = px.line(df_rent_avg, x='city', y='rent amount (R$)', 
                       title='Comparativo de Valores de Aluguel por Cidade',
                       labels={'rent amount (R$)': 'Valor Médio do Aluguel (R$)', 'city': 'Cidade'},
                       markers=True, height=400, 
                       color_discrete_sequence=['#FF6347'])

    fig_rent.update_layout(
        xaxis=dict(showline=False, showgrid=False),
        yaxis=dict(showline=False, showgrid=False),
        plot_bgcolor='rgba(0,0,0,0)'  
    )

    st.plotly_chart(fig_rent, use_container_width=True)
else:
    st.write("Nenhum dado disponível para o gráfico de valores de aluguel.")

