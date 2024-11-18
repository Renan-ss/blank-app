import streamlit as st
import pandas as pd
import requests

# Substitua pela sua chave de API do SimilarWeb
API_KEY = '085f32c594cc48fd924a8a861f24af96'  # Substitua por sua chave de API real

# Função para obter os sites mais acessados de um país
def get_top_sites(country_code):
    url = f'https://api.similarweb.com/v1/country/{country_code}/top-websites'
    
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    
    # Realiza a requisição para a API
    response = requests.get(url, headers=headers)
    
    # Verifica se a requisição foi bem sucedida
    if response.status_code == 200:
        return response.json()['data']  # Retorna a lista de sites
    else:
        st.error(f'Erro ao buscar dados para {country_code}: {response.status_code}')
        return []

# Função para organizar os dados em DataFrame
def create_dataframe(data):
    # O formato dos dados pode variar, então é necessário ajustar conforme a estrutura real da resposta
    # Assumindo que os dados retornados tenham as chaves 'rank', 'domain', e 'traffic'
    df = pd.DataFrame(data)
    df.columns = ['Posição', 'Site', 'Acessos']  # Ajuste de acordo com os dados reais retornados
    return df

# Cabeçalho
st.title('Top 20 Sites Mais Acessados por País')

# Filtro de Países
pais_selecionado = st.sidebar.selectbox(
    'Selecione o país',
    ['Brasil', 'China', 'Estados Unidos', 'Japão', 'Alemanha']
)

# Mapear países para seus códigos ISO 3166-1 Alpha-2 (Simbolos ISO)
country_codes = {
    'Brasil': 'BR',
    'China': 'CN',
    'Estados Unidos': 'US',
    'Japão': 'JP',
    'Alemanha': 'DE'
}

# Obter os dados de top sites
country_code = country_codes[pais_selecionado]
top_sites_data = get_top_sites(country_code)

if top_sites_data:
    # Criando o DataFrame com os dados
    df = create_dataframe(top_sites_data)
    
    # Exibindo a tabela de dados
    st.write(f'Top 20 Sites Mais Acessados no {pais_selecionado}')
    st.dataframe(df)
    
    # Criando o gráfico de barras de acessos (assumindo que "Acessos" é um campo disponível)
    st.subheader(f'Acessos dos Top 20 Sites no {pais_selecionado}')
    st.bar_chart(df.set_index('Posição')['Acessos'])
else:
    st.write('Não foi possível obter os dados. Tente novamente mais tarde.')
