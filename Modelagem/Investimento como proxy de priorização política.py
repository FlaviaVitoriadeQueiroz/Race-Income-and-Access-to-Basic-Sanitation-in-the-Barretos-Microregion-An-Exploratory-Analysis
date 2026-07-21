'''Correlação entre perc_negra e investimento per capita (investimento ÷ Total) — atenção 
aos NaN em Colina, Guaraci e Monte Azul Paulista, que vão reduzir o N disponível pra essa 
análise específica.
Esse é o achado com mais "força de manchete" pra apresentação: mostra alocação de recursos, 
não só resultado.'''


'''É a ideia de usar a coluna investimento (do SNIS) como um substituto indireto para medir 
se o poder público está priorizando ou não certos municípios em saneamento — já que você não 
tem uma variável direta de "prioridade política", mas tem quanto dinheiro foi de fato investido 
em cada lugar.

A lógica por trás:
Renda mede o poder de compra das famílias; já investimento público mede uma decisão do Estado — 
quanto ele decidiu aplicar em infraestrutura de saneamento naquele município, naquele ano. Se 
municípios com maior perc_negra recebem sistematicamente menos investimento por habitante do que 
municípios com menor perc_negra, isso é evidência (ainda que indireta) de que a alocação de 
recursos públicos não é neutra em relação à composição racial da população — é um padrão
consistente com o que a literatura chama de "racismo ambiental" ou desigualdade na provisão de 
infraestrutura.

Por que "proxy" e não "prova direta":
Investimento é influenciado por várias coisas além de composição racial — tamanho do município, 
gestão local, prioridades técnicas (ex. rede já estar mais deteriorada em um lugar), ciclo eleitoral, 
capacidade de captar recursos estaduais/federais, etc. Então uma correlação entre perc_negra e 
investimento per capita não prova que a decisão foi motivada por raça — mas é um dado concreto e 
verificável (não uma estimativa, como a renda), que aponta na direção de "quem recebe menos recursos".'''


from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from utils import carregar_base_por_municipio
 
df_mun = carregar_base_por_municipio()
 
sub_invest = df_mun[["municipio", "perc_negra", "investimento_per_capita"]].dropna()
print(sub_invest.sort_values("investimento_per_capita"))
 
if len(sub_invest) > 2:
    r, p = stats.spearmanr(sub_invest["perc_negra"], sub_invest["investimento_per_capita"])
    print(f"\nSpearman perc_negra x investimento_per_capita: r={r:.3f}, p={p:.3f} (N={len(sub_invest)})")
else:
    print("\nN insuficiente para correlação após remover NaN.")
 
plt.figure(figsize=(7, 5))
sns.scatterplot(data=sub_invest, x="perc_negra", y="investimento_per_capita")
for _, row in sub_invest.iterrows():
    plt.annotate(row["municipio"], (row["perc_negra"], row["investimento_per_capita"]), fontsize=8)
plt.title("Investimento per capita médio x % população negra")
plt.xlabel("% população negra (preta + parda)")
plt.ylabel("Investimento per capita médio (R$)")
plt.tight_layout()
plt.savefig("scatter_investimento_racial.png", dpi=150)
plt.close()
print("[salvo] scatter_investimento_racial.png")