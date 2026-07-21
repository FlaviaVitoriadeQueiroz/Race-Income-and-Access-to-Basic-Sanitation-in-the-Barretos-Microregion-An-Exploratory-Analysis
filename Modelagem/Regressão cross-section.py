# Essa é a técnica mais adequada dado que renda e raça são fixas por município:

'''Essa é a técnica mais adequada dado que renda e raça são fixas por município:
OLS múltiplo: índice de saneamento (médio 2013-2022) ~ perc_negra + renda_media_estimada.
Com N=9 e 2 preditores, você está no limite do que é estatisticamente defensável (regra 
prática seria pelo menos ~15 obs para 2 preditores). Rode, mas trate o resultado como 
descritivo/exploratório, não como prova estatística robusta — deixe isso explícito no 
relatório.
Rodar separadamente cada índice como variável dependente (água, esgoto coleta, esgoto 
tratamento, perda) em vez de um índice composto, já que eles têm dinâmicas bem diferentes 
(ex. Monte Azul Paulista tem tratamento de esgoto baixíssimo mas água/coleta ok).
Correlação parcial entre perc_negra e cada índice, controlando renda_media_estimada — é 
uma forma mais simples que regressão múltipla de testar "será que sobra associação racial 
depois de tirar o efeito de renda?", e funciona melhor com N pequeno.'''

import numpy as np
from utils import carregar_base_por_municipio, ols, resumo_regressao, correlacao_parcial, INDICES
 
df_mun = carregar_base_por_municipio()
 
for idx in INDICES:
    print(f"\n--- Variável dependente: {idx} ---")
 
    sub = df_mun[[idx, "perc_negra", "renda_media_estimada"]].dropna()
    X = np.column_stack([np.ones(len(sub)), sub["perc_negra"].values, sub["renda_media_estimada"].values])
    y = sub[idx].values
    beta, se, residuos, _ = ols(X, y)
    resumo = resumo_regressao(["const", "perc_negra", "renda_media_estimada"], beta, se, len(sub), X.shape[1])
    print(resumo.round(4))
 
    r_parcial, p_parcial = correlacao_parcial(df_mun, "perc_negra", idx, "renda_media_estimada")
    print(f"Correlação parcial (perc_negra x {idx} | renda): r={r_parcial:.3f}, p={p_parcial:.3f}")