import pandas as pd

# Carregando as bases de dados tratadas
snis = pd.read_csv("snis_tratado.csv", encoding="utf-8-sig")

ibge = pd.read_csv("renda_raca_censo_tratado.csv", encoding="utf-8-sig")


#Padronizando 
snis["municipio"] = (snis["municipio"].str.upper().str.strip())

ibge["municipio"] = (ibge["municipio"].str.upper().str.strip())

base = snis.merge(ibge, on="municipio", how="left")


# Indicadores 
base["investimento_per_capita"] = (base["investimento"] /base["Total"])
base["agua_per_capita"] = (base["pop_agua"] /base["Total"])
base["esgoto_per_capita"] = (base["pop_esgoto"] /base["Total"])
base["agua_nao_atendida"] = (base["Total"] -base["pop_agua"])
base["esgoto_nao_atendido"] = (base["Total"] -base["pop_esgoto"])
base["perc_sem_agua"] = (100 -base["indice_agua"])
base["perc_sem_esgoto"] = (100 -base["indice_coleta_esgoto"])


# Organizando
base = base.sort_values(["municipio","ano"])


#Merge
df_final = pd.merge(snis,ibge,on="municipio",how="inner")


# Verificando o resultado do merge

print("=" * 50)
print("RESULTADO DO MERGE")
print("=" * 50)

print(f"\nMunicípios SNIS : {len(snis)}")
print(f"Municípios IBGE : {len(ibge)}")
print(f"Municípios Merge: {len(df_final)}")

print("\nColunas:")
print(df_final.columns.tolist())

print("\nPrimeiras linhas:")
print(df_final.head())

print("\nValores ausentes:")
print(df_final.isnull().sum())


# Salvando a base final

df_final.to_csv("base_final.csv", index=False, encoding="utf-8-sig")

print("\nBase final salva com sucesso!")