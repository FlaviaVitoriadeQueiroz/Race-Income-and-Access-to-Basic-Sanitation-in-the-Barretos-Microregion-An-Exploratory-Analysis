'''Como perc_negra e renda_media_estimada não variam no tempo, efeitos fixos de 
município vão absorver esses efeitos e zerar os coeficientes — não use FE de 
município como abordagem principal aqui.
Alternativa que funciona: efeitos fixos de ano apenas (controla choques nacionais 
tipo pandemia 2020-2021) com erros-padrão clusterizados por município, mantendo 
raça/renda como preditores. Isso aproveita a variação temporal dos índices sem 
descartar suas variáveis de interesse.
Serve principalmente para checar se a associação é estável ao longo dos anos ou 
concentrada em períodos específicos (ex.: será que a diferença fica pior justamente 
nos anos de corte de investimento?).'''

import pandas as pd
from utils import carregar_base, ols_cluster_robust_se, INDICES
 
df = carregar_base()
df_painel = df.dropna(subset=["perc_negra", "renda_media_estimada"]).copy()
 
for idx in INDICES:
    sub = df_painel.dropna(subset=[idx]).copy()
    if sub.empty:
        continue
 
    dummies_ano = pd.get_dummies(sub["ano"], prefix="ano", drop_first=True).astype(float)
    X = pd.concat(
        [pd.Series(1.0, index=sub.index, name="const"), sub[["perc_negra", "renda_media_estimada"]], dummies_ano],
        axis=1,
    )
    nomes = X.columns.tolist()
    y = sub[idx].values
 
    beta, se, residuos = ols_cluster_robust_se(X.values, y, sub["municipio"].values)
    resumo = pd.DataFrame({"coef": beta, "erro_padrao_cluster": se}, index=nomes)
 
    print(f"\n--- Variável dependente: {idx} ---")
    print(resumo.loc[["perc_negra", "renda_media_estimada"]].round(4))