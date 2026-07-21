# Correlação de Spearman
'''entre perc_negra, renda_media_estimada e cada índice (indice_agua, indice_coleta_esgoto, 
indice_tratamento_esgoto, indice_perda_agua). Spearman em vez de Pearson porque você tem poucos 
pontos e possíveis outliers (Guaraci e Severínia têm tratamento de esgoto muito baixo, por exemplo).'''

# Matriz de correlação
'''com todas essas variáveis de uma vez — dá uma visão geral rápida de quais pares merecem atenção antes de 
qualquer modelo.
Como renda_media_estimada é praticamente fixa por município (vem do Censo 2022, não varia no tempo), essa 
correlação já deveria ser feita numa base colapsada por município (uma linha por cidade, com média dos índices 
ao longo dos anos), não no painel completo — senão você está pseudo-repetindo a mesma renda 10 vezes por município 
e inflando artificialmente o N.'''


# Correlação de Spearman + heatmap (nível município)
 
import matplotlib.pyplot as plt
import seaborn as sns
from utils import carregar_base_por_municipio, matriz_pvalor_spearman, INDICES
 
df_mun = carregar_base_por_municipio()
 
variaveis_corr = ["perc_negra", "renda_media_estimada", "investimento_per_capita"] + INDICES
corr_matrix = df_mun[variaveis_corr].corr(method="spearman")
 
print("Correlação de Spearman:")
print(corr_matrix.round(2))
 
pval_matrix = matriz_pvalor_spearman(df_mun, variaveis_corr)
print("\nMatriz de p-valores:")
print(pval_matrix.round(3))
 
plt.figure(figsize=(9, 7))
sns.heatmap(corr_matrix, annot=True, cmap="RdBu_r", center=0, vmin=-1, vmax=1, fmt=".2f")
plt.title("Correlação de Spearman — raça, renda, investimento e saneamento\n(nível município, N=9)")
plt.tight_layout()
plt.savefig("heatmap_correlacao.png", dpi=150)
plt.close()
print("\n[salvo] heatmap_correlacao.png")

