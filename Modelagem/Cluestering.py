'''Hierárquico (Ward) com perc_negra, renda_media_estimada e os índices médios 
— dendrograma é fácil de interpretar com só 9 casos e visualmente forte pro dashboard.
Serve pra classificar municípios em grupos tipo "alta vulnerabilidade racial/renda + 
saneamento ruim" vs. "baixa vulnerabilidade + saneamento bom", sem alegar causalidade — 
é só descrição de padrão.'''

import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from utils import carregar_base_por_municipio, INDICES
 
df_mun = carregar_base_por_municipio()
 
vars_cluster = ["perc_negra", "renda_media_estimada"] + INDICES
dados_cluster = df_mun.set_index("municipio")[vars_cluster].dropna()
 
# padronizando (z-score) — essencial para renda (escala em R$) não dominar a distância
dados_padronizados = (dados_cluster - dados_cluster.mean()) / dados_cluster.std()
 
Z = linkage(dados_padronizados, method="ward")
 
plt.figure(figsize=(10, 6))
dendrogram(Z, labels=dados_padronizados.index.tolist(), leaf_rotation=45)
plt.title("Dendrograma — tipologia de municípios\n(raça, renda estimada e indicadores de saneamento)")
plt.ylabel("Distância (Ward)")
plt.tight_layout()
plt.savefig("dendrograma_clusters.png", dpi=150)
plt.close()
print("[salvo] dendrograma_clusters.png")
 
# Ajuste K conforme a leitura visual do dendrograma
K = 3
grupos = fcluster(Z, K, criterion="maxclust")
df_mun_cluster = dados_cluster.copy()
df_mun_cluster["grupo"] = grupos
 
print(f"\nGrupos (K={K}):")
print(df_mun_cluster.sort_values("grupo"))