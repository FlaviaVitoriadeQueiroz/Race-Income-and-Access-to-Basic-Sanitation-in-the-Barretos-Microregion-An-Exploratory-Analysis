import os
import pandas as pd
import numpy as np
from scipy import stats
 
# Caminho calculado a partir da localização deste arquivo (utils.py), não da
# pasta de onde o script é executado — evita erro de "arquivo não encontrado"
# dependendo de como/de onde você roda o script (terminal, VS Code, duplo-clique).
# O CSV está na MESMA pasta que utils.py (Modelagem/), com o nome base_final.csv.
PASTA_DESTE_ARQUIVO = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BASE = os.path.join(PASTA_DESTE_ARQUIVO, "base_final.csv")
INDICES = ["indice_agua", "indice_coleta_esgoto", "indice_tratamento_esgoto", "indice_perda_agua"]
 
 
def carregar_base(caminho=CAMINHO_BASE):
    """Carrega o painel (ano x município) já mesclado (SNIS + raça + renda)."""
    return pd.read_csv(caminho)
 
 
def carregar_base_por_municipio(caminho=CAMINHO_BASE):
    """Colapsa o painel para uma linha por município — usa a média dos índices
    ao longo dos anos, e mantém fixos perc_negra/renda_media_estimada (que não
    variam no tempo). Também calcula investimento_per_capita médio."""
    df = carregar_base(caminho)
    df_mun = (
        df.groupby("municipio")
        .agg(
            indice_agua=("indice_agua", "mean"),
            indice_coleta_esgoto=("indice_coleta_esgoto", "mean"),
            indice_tratamento_esgoto=("indice_tratamento_esgoto", "mean"),
            indice_perda_agua=("indice_perda_agua", "mean"),
            investimento_medio=("investimento", "mean"),
            Total=("Total", "first"),
            perc_negra=("perc_negra", "first"),
            renda_media_estimada=("renda_media_estimada", "first"),
        )
        .reset_index()
    )
    df_mun["investimento_per_capita"] = df_mun["investimento_medio"] / df_mun["Total"]
    return df_mun
 
 
# ---------------------------------------------------------------
# Regressão OLS manual (sem statsmodels)
# ---------------------------------------------------------------
 
def ols(X, y):
    """OLS via mínimos quadrados. X já deve incluir a coluna de constante (1s).
    Retorna beta, erros-padrão clássicos, resíduos e (X'X)^-1."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    residuos = y - X @ beta
    sigma2 = (residuos @ residuos) / (n - k)
    se_classico = np.sqrt(np.diag(sigma2 * XtX_inv))
    return beta, se_classico, residuos, XtX_inv
 
 
def ols_cluster_robust_se(X, y, clusters):
    """Erros-padrão clusterizados (cluster-robust sandwich estimator)."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    residuos = y - X @ beta
 
    clusters = np.asarray(clusters)
    meio = np.zeros((k, k))
    for g in np.unique(clusters):
        idx = clusters == g
        Xg = X[idx]
        eg = residuos[idx]
        score_g = Xg.T @ eg
        meio += np.outer(score_g, score_g)
 
    n_clusters = len(np.unique(clusters))
    correcao = (n_clusters / (n_clusters - 1)) * ((n - 1) / (n - k))
    V = correcao * XtX_inv @ meio @ XtX_inv
    se = np.sqrt(np.diag(V))
    return beta, se, residuos
 
 
def resumo_regressao(nomes_coef, beta, se, n, k):
    t = beta / se
    p = 2 * (1 - stats.t.cdf(np.abs(t), df=n - k))
    return pd.DataFrame({"coef": beta, "erro_padrao": se, "t": t, "p_valor": p}, index=nomes_coef)
 
 
def correlacao_parcial(data, x, y, controle):
    """Correlação parcial entre x e y controlando 'controle', via resíduos de regressões lineares simples."""
    sub = data[[x, y, controle]].dropna()
    Xc = np.column_stack([np.ones(len(sub)), sub[controle].values])
    beta_x, _, _, _ = ols(Xc, sub[x].values)
    beta_y, _, _, _ = ols(Xc, sub[y].values)
    res_x = sub[x].values - Xc @ beta_x
    res_y = sub[y].values - Xc @ beta_y
    r, p = stats.pearsonr(res_x, res_y)
    return r, p
 
 
def matriz_pvalor_spearman(data, cols):
    n = len(cols)
    pmat = pd.DataFrame(np.ones((n, n)), index=cols, columns=cols)
    for i in cols:
        for j in cols:
            if i != j:
                sub = data[[i, j]].dropna()
                if len(sub) > 2:
                    _, p = stats.spearmanr(sub[i], sub[j])
                    pmat.loc[i, j] = p
    return pmat