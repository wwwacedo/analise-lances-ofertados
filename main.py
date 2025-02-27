import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def formatar_real(valor):
    """Formata um número float como moeda brasileira (R$)."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# VARIÁVEIS LOCAIS
percentil_outliers = 95

# Substitua pelo nome correto do seu arquivo
file_path = "lances.xlsx"

# Carregar a planilha
df = pd.read_excel(file_path)

# Converter a coluna 'Data/Hora' para datetime
df["Sequência de Lances"] = range(1, len(df) + 1)

# Criar a figura do gráfico
plt.figure(figsize=(16, 8))

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
    subset = df_filtrado[df_filtrado["Licitante"] == licitante]  # Filtrar os dados do licitante

    # Criar o gráfico de degraus (step plot)
    plt.step(
        subset["Sequência de Lances"],  # Usando números sequenciais no eixo X
        subset["Valor"],
        where="post",
        linewidth=1,
        label=licitante,
    )

    # Adicionar os números da sequência nos pontos do gráfico
    for x, y in zip(subset["Sequência de Lances"], subset["Valor"]):
        plt.text(x, y, str(x), fontsize=8, ha="right", va="bottom")  # Ajuste de posição


# Configurações do gráfico
plt.xlabel("Sequência de Lances")
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
"""
plt.legend(
    title="Licitante",
    loc="upper right",   # Posiciona no canto superior direito dentro do gráfico
    bbox_to_anchor=(1, 1),  # Pequeno deslocamento interno
    facecolor="white",  # Fundo branco para melhor legibilidade
    edgecolor="black",  # Borda preta
    fontsize=10,        # Tamanho da fonte ajustado
    framealpha=0.8      # Transparência para não cobrir os dados completamente
)

"""

# Melhorar a distribuição dos dados
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# Ajustar layout para melhor visualização
plt.tight_layout()

# Calcular estatísticas dos valores dos lances
media = df_filtrado["Valor"].mean()
mediana = df_filtrado["Valor"].median()
valor_maximo = df_filtrado["Valor"].max()
valor_minimo = df_filtrado["Valor"].min()

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

# Mostrar o gráfico ajustado
plt.show()



