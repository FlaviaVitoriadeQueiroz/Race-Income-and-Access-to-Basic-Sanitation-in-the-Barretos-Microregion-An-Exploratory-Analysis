import pandas as pd

# Carregando o arquivo CSV original
df = pd.read_csv("renda_raca_censo.csv",sep=";",encoding="utf-8")

# Limpando nomes de colunas (removendo espaços extras)
df.columns = df.columns.str.strip()


# Limpeza do nome dos municípios (removendo "(SP)" e espaços extras)
df["Município"] = (df["Município"].str.replace(r"\s*\(SP\)", "", regex=True).str.strip())


# Convertendo colunas numéricas para float, substituindo "-" por 0 e preenchendo NaN com 0
cols = ["Total", "Branca", "Preta", "Amarela", "Parda", "Indígena"]

for col in cols:
    df[col] = (df[col].replace("-",0).fillna(0).astype(float))


# Mantendo apenas as linhas onde a classe de rendimento seja "Total"
df = df[df["Classes de rendimento nominal mensal domiciliar per capita"] == "Total"].copy()


# Criando indicadores de percentual de cada etnia em relação ao total
df["perc_branca"] = (df["Branca"] / df["Total"])
df["perc_preta"] = (df["Preta"] / df["Total"])
df["perc_parda"] = (df["Parda"] / df["Total"])
df["perc_indigena"] = (df["Indígena"] / df["Total"])
df["perc_negra"] = ((df["Preta"] + df["Parda"]) / df["Total"])


# Selecionando apenas as colunas de interesse
df = df[["Município", "Total", "Branca", "Preta", "Parda", "Indígena", "perc_branca", "perc_preta", "perc_parda", "perc_indigena", "perc_negra"]]


# Renomeando a coluna "Município" para "municipio" para facilitar o merge com a base do SNIS
df.rename(columns={"Município":"municipio"},inplace=True)



# Verificar se há municípios duplicados
duplicados = df["municipio"].duplicated().sum()
print(f"Municípios duplicados: {duplicados}")


# Visualizar os primeiros registros e informações gerais do DataFrame
print(df.head())
print(df.info())


# Salvando
df.to_csv("renda_raca_censo_tratado.csv", index=False, encoding="utf-8-sig")