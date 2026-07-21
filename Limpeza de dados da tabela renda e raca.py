import pandas as pd

# Carregando o arquivo CSV original
df = pd.read_csv("renda_raca_censo.csv", sep=";", encoding="utf-8")

# Limpando nomes de colunas (removendo espaços extras)
df.columns = df.columns.str.strip()

# Limpeza do nome dos municípios (removendo "(SP)" e espaços extras)
df["Município"] = (df["Município"].str.replace(r"\s*\(SP\)", "", regex=True).str.strip())

# Convertendo colunas numéricas para float, substituindo "-" por 0 e preenchendo NaN com 0
cols = ["Total", "Branca", "Preta", "Amarela", "Parda", "Indígena"]

for col in cols:
    df[col] = (df[col].replace("-", 0).fillna(0).astype(float))

# Cálculo da renda média estimada por município 

SALARIO_MINIMO = 1212

# Ponto médio de cada faixa, em número de salários mínimos
# "Mais de 20 salários mínimos" é faixa aberta: usamos 25 SM como convenção
pontos_medios_sm = {
    "Até 1/4 de salário mínimo": 0.125,
    "Mais de 1/4 a 1/2 salário mínimo": 0.375,
    "Mais de 1/2 a 1 salário mínimo": 0.75,
    "Mais de 1 a 2 salários mínimos": 1.5,
    "Mais de 2 a 3 salários mínimos": 2.5,
    "Mais de 3 a 5 salários mínimos": 4.0,
    "Mais de 5 a 10 salários mínimos": 7.5,
    "Mais de 10 a 15 salários mínimos": 12.5,
    "Mais de 15 a 20 salários mínimos": 17.5,
    "Mais de 20 salários mínimos": 25.0,
    "Sem rendimento": 0.0,
}

# Filtrando apenas as linhas de faixas de renda (excluindo a linha "Total")
df_faixas = df[df["Classes de rendimento nominal mensal domiciliar per capita"] != "Total"].copy()

# Mapeando cada faixa para seu ponto médio em reais
df_faixas["ponto_medio_reais"] = (df_faixas["Classes de rendimento nominal mensal domiciliar per capita"].map(pontos_medios_sm) * SALARIO_MINIMO)

# Renda ponderada = ponto médio da faixa * número de pessoas na faixa (coluna Total)
df_faixas["renda_ponderada"] = df_faixas["ponto_medio_reais"] * df_faixas["Total"]

# Agrupando por município: soma da renda ponderada / soma do total de pessoas nas faixas
renda_media = (
df_faixas.groupby("Município").apply(lambda g: g["renda_ponderada"].sum() / g["Total"].sum()).reset_index(name="renda_media_estimada"))


# Mantendo apenas as linhas onde a classe de rendimento seja "Total"
df = df[df["Classes de rendimento nominal mensal domiciliar per capita"] == "Total"].copy()

# Criando indicadores de percentual de cada etnia em relação ao total
df["perc_branca"] = (df["Branca"] / df["Total"])
df["perc_preta"] = (df["Preta"] / df["Total"])
df["perc_parda"] = (df["Parda"] / df["Total"])
df["perc_indigena"] = (df["Indígena"] / df["Total"])
df["perc_negra"] = ((df["Preta"] + df["Parda"]) / df["Total"])

# Juntando a renda média estimada ao dataframe principal
df = df.merge(renda_media, on="Município", how="left")

# Selecionando apenas as colunas de interesse
df = df[["Município", "Total", "Branca", "Preta", "Parda", "Indígena",
         "perc_branca", "perc_preta", "perc_parda", "perc_indigena", "perc_negra",
         "renda_media_estimada"]]

# Renomeando a coluna "Município" para "municipio" para facilitar o merge com a base do SNIS
df.rename(columns={"Município": "municipio"}, inplace=True)

# Verificar se há municípios duplicados
duplicados = df["municipio"].duplicated().sum()
print(f"Municípios duplicados: {duplicados}")

# Visualizar os primeiros registros e informações gerais do DataFrame
print(df.head())
print(df.info())

# Salvando
df.to_csv("renda_raca_censo_tratado.csv", index=False, encoding="utf-8-sig")