import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def formatar_real(valor):
    """Formata um número float como moeda brasileira (R$)."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# VARIÁVEIS LOCAIS
percentil_outliers = 100 #100% para não remover nenhum valor

# Substitua pelo nome correto do seu arquivo
file_path = "lances.xlsx"

# Carregar a planilha
df = pd.read_excel(file_path)

# Ordenar pelo tempo e criar a sequência de lances
df = df.sort_values(by="Data/Hora").reset_index(drop=True)
df["Sequência de Lances"] = range(1, len(df) + 1)

# Converter a coluna 'Data/Hora' para datetime
df["Data/Hora"] = pd.to_datetime(df["Data/Hora"], dayfirst=True)

# Calcular o tempo em minutos desde o primeiro lance
tempo_inicial = df["Data/Hora"].min()
df["Minutos"] = df["Data/Hora"].apply(lambda x: (x - tempo_inicial).total_seconds() / 60)

# Criar a figura do gráfico
plt.figure(figsize=(23.4, 16.5))  # A2 em polegadas

# Obter os nomes dos licitantes únicos
licitantes = df["Licitante"].unique()

# Definir limite superior para evitar distorções
limite_inferior = df["Valor"].min()  # Menor valor presente nos lances
limite_superior = np.percentile(df["Valor"], percentil_outliers)  # Filtramos valores muito altos

# Filtrar o DataFrame removendo valores acima do percentil 
df_filtrado = df[df["Valor"] <= limite_superior]
    
# Filtrar o DataFrame removendo valores acima do percentil
df_invalido = df[df["Valor"] > limite_superior]

if not df_invalido.empty:
    print(f"🚨 Foram encontrados lances inválidos acima do percentil {percentil_outliers}!")
    for _, linha in df_invalido.iterrows():  # Itera corretamente sobre as linhas do DataFrame
        print(f"\t - {linha['Licitante'][:20]}........\t{formatar_real(linha['Valor'])}")


# Plotar uma linha para cada licitante
for licitante in licitantes:
    subset = df_filtrado[df_filtrado["Licitante"] == licitante]

    # Plotando o passo temporal com valor
    plt.step(
        subset["Minutos"],
        subset["Valor"],
        where="post",
        linewidth=1,
        label=licitante,
    )

    # Adiciona o número sequencial como rótulo no ponto
    for x, y, seq in zip(subset["Minutos"], subset["Valor"], subset["Sequência de Lances"]):
        plt.text(x, y, str(seq), fontsize=8, ha="right", va="bottom")


# Configurações do gráfico
plt.xlabel("Minutos desde o primeiro lance")
plt.ylabel("Valor do Lance (R$)")
plt.title("Evolução dos Lances ao Longo do Tempo")
plt.xticks(rotation=60)  # Ajusta a rotação das datas no eixo X

# Definir o limite superior do eixo Y para evitar achatamento
#plt.yscale("log")
plt.ylim(limite_inferior, limite_superior)

print(limite_inferior, limite_superior) 

# Formatar os valores do eixo Y como reais (R$)
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'R$ {x:,.2f}'))

# Adicionar a legenda dentro do gráfico
plt.legend(
    title="Licitante",
    loc="upper right",   # Posiciona no canto superior direito dentro do gráfico
    bbox_to_anchor=(1, 1),  # Pequeno deslocamento interno
    facecolor="white",  # Fundo branco para melhor legibilidade
    edgecolor="black",  # Borda preta
    fontsize=5,        # Tamanho da fonte ajustado
    framealpha=0.8      # Transparência para não cobrir os dados completamente
)

# Melhorar a distribuição dos dados
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# Ajustar layout para melhor visualização
plt.tight_layout()

# Calcular estatísticas dos valores dos lances
media = df_filtrado["Valor"].mean()
mediana = df_filtrado["Valor"].median()
valor_maximo = df_filtrado["Valor"].max()
valor_minimo = df_filtrado["Valor"].min()

# Adicionar estatísticas como "segunda legenda"
texto_estatisticas = (
    f"Média: {formatar_real(media)}\n"
    f"Mediana: {formatar_real(mediana)}\n"
    f"Máximo: {formatar_real(valor_maximo)}\n"
    f"Mínimo: {formatar_real(valor_minimo)}"
)

# Adiciona o texto dentro do gráfico no canto inferior direito
plt.gcf().text(
    0.53, 0.93, texto_estatisticas,
    ha='center', va='top',
    fontsize=10,
    bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.5')
)

# Exibir relatório formatado corretamente
relatorio = f"""
📊 **Relatório Estatístico dos Lances**
--------------------------------------
🔹 Média aritmética simples: {formatar_real(media)}
🔹 Mediana: {formatar_real(mediana)}
🔹 Valor Máximo: {formatar_real(valor_maximo)}
🔹 Valor Mínimo: {formatar_real(valor_minimo)}
"""
print(relatorio)

# Salvar o gráfico como imagem em tamanho A2 com alta qualidade
plt.savefig("grafico_lances_A2.png", dpi=300, bbox_inches="tight", format="png")

# Mostrar o gráfico ajustado
plt.show()



