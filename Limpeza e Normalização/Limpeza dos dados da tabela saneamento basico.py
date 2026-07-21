import pandas as pd
import requests

# Definindo o ano de análise e os municípios da região de Barretos
ANO_INICIAL = 2013

cidades_regiao = ["Barretos", "Bebedouro", "Colina", "Colômbia", "Guaraci", "Jaborandi", "Monte Azul Paulista",
    "Olímpia", "Severínia", "Terra Roxa"]


# Arquivo CSV do SNIS (Sistema Nacional de Informações sobre Saneamento) com os dados de saneamento básico
df = pd.read_csv("tabela saneamento basico.csv")


# Últimos 10 anos
df = df[df["ano"] >= ANO_INICIAL].copy()


# Buscando os códigos IBGE dos municípios da região de Barretos via API do IBGE

url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/SP/municipios"

municipios = requests.get(url).json()
df_municipios = pd.DataFrame([{"codigo_ibge": m["id"], "municipio": m["nome"]} for m in municipios])
df_municipios = df_municipios[df_municipios["municipio"].isin(cidades_regiao)]


# Filtrando apenas os municípios da região de Barretos
codigos = df_municipios["codigo_ibge"].tolist()
df = df[df["id_municipio"].isin(codigos)]


# Merge
df = df.merge( df_municipios, left_on="id_municipio", right_on="codigo_ibge", how="left")


# Removendo colunas desnecessárias
df.drop(columns=["id_municipio", "codigo_ibge"],inplace=True)


# Removendo acentos e convertendo para minúsculas
df.rename(columns={"sigla_uf": "uf", "populacao_urbana": "pop_urbana", "populacao_atendida_agua": "pop_agua",
    "populacao_atentida_esgoto": "pop_esgoto", "indice_atendimento_urbano_agua": "indice_agua",
    "indice_coleta_esgoto": "indice_coleta_esgoto", "indice_tratamento_esgoto": "indice_tratamento_esgoto",
    "indice_perda_distribuicao_agua": "indice_perda_agua", "investimento_total_prestador": "investimento"}, inplace=True)


print(df.head())
# Mantendo apenas as colunas de interesse
df = df[["ano", "municipio", "uf", "pop_urbana", "pop_agua", "pop_esgoto", "indice_agua", "indice_coleta_esgoto", 
         "indice_tratamento_esgoto", "indice_perda_agua", "investimento"]]


# Ordenando por município e resetando o índice
df = df.sort_values("municipio").reset_index(drop=True)


# Verificando os valores ausentes e duplicados
print("\nValores ausentes:")
print(df.isnull().sum())
print("\nMunicípios duplicados:")
print(df["municipio"].duplicated().sum())
print("\nPrévia da base:")
print(df.head())


# Salvando 
df.to_csv("snis_tratado.csv", index=False, encoding="utf-8-sig")
print("\nArquivo salvo com sucesso: snis_tratado.csv")
