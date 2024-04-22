import streamlit as st
import requests
import pandas as pd
import time

@st.cache_data
def converte_csv(df):
    return df.to_csv(index = False).encode('utf-8')

def mensagem_sucesso():
    sucesso = st.success('Download finalizado!', icon = "✅")
    time.sleep(7)
    sucesso.empty()


st.title('DADOS BRUTOS')

url = 'https://labdados.com/produtos'

response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')

st.sidebar.title('Filtros')

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas',list(dados.columns), list(dados.columns))


with st.sidebar.expander('Nome do produto'):
    produtos = st.multiselect('Selecione os produtos', dados['Produto'].unique(), dados['Produto'].unique())

with st.sidebar.expander('Categorias'):
  categorias = st.multiselect('Selecione os produtos', dados['Categoria do Produto'].unique(), dados['Categoria do Produto'].unique())

with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço',0, 5000, (0, 5000))

with st.sidebar.expander('Frete da venda'):
    frete = st.slider('Frete', 0, 250, (0, 250))    

with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))

with st.sidebar.expander('Vendedores'):
    vendedores = st.multiselect('Selecione os vendedores', dados['Vendedor'].unique(), dados['Vendedor'].unique())

with st.sidebar.expander('Regiões'):
    regioes = st.selectbox('Selecione a região desejada', dados['Local da compra'])    

with st.sidebar.expander('Avaliações'):
    avaliações = st.multiselect('Selecione a avaliação desejada', dados['Avaliação da compra'].unique(), dados['Avaliação da compra'].unique())

with st.sidebar.expander('Tipo de pagamento'):
    tipo_pagamento = st.multiselect('Selecione a forma de pagamento', dados['Tipo de pagamento'].unique(), dados['Tipo de pagamento'].unique())

with st.sidebar.expander('Quantidade de parcelas'):
    parcelas = st.slider('Selecione a quantidade de parcelas', 0, 24, (0, 24))    



query = '''
Produto in @produtos and \
`Categoria do Produto` in @categorias and \
@preco[0] <= Preço <= @preco[1] and \
@frete[0] <= Frete <= @frete[1] and \
@data_compra[0] <=`Data da Compra` <= @data_compra[1] and \
Vendedor in @vendedores and \
`Local da compra` in @regioes and \
`Avaliação da compra` in @avaliações and \
`Tipo de pagamento` in @tipo_pagamento and \
@parcelas[0] <= `Quantidade de parcelas` <= @parcelas[1]
'''

dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}] colunas.')

st.markdown('Escreva um nome para o arquivo: ')
col1, col2 = st.columns(2)

with col1:
    nome_arquivo = st.text_input('', label_visibility = 'collapsed', value = 'dados')
    nome_arquivo += '.csv'

with col2:
    st.download_button('Fazer download da tabela em CSV', data = converte_csv(dados_filtrados), file_name = nome_arquivo,
                       mime = 'text/csv', on_click = mensagem_sucesso)
