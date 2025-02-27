import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Substitua pelo nome correto do seu arquivo
file_path = "lances.xlsx"

# Carregar a planilha
df = pd.read_excel(file_path)

# Converter a coluna 'Data/Hora' para datetime
df['Data/Hora'] = df['Data/Hora'].astype(str).str.replace('\n', ' ')  # Remove a quebra de linha
df['Data/Hora'] = pd.to_datetime(df['Data/Hora'], format="%d/%m/%Y %H:%M:%S", dayfirst=True)

# Remover possíveis formatações e converter 'Valor' para número
df['Valor'] = df['Valor'].astype(str).str.replace('.', '').str.replace(',', '.').astype(float)

# Criar a figura do gráfico
plt.figure(figsize=(16, 8))

# Obter os nomes dos licitantes únicos
licitantes = df["Licitante"].unique()

# Definir limite superior para evitar distorções
limite_inferior = df["Valor"].min()  # Menor valor presente nos lances
limite_superior = np.percentile(df["Valor"], 99)  # Filtramos valores muito altos

# Filtrar o DataFrame removendo valores acima do percentil 99
df_filtrado = df[df["Valor"] <= limite_superior]

# Filtrar o DataFrame removendo valores acima do percentil 99
df_invalido = df[df["Valor"] >= limite_superior]
print(f"Valores acima do percentil 99:\n{df_invalido}")

# Plotar uma linha para cada licitante
for licitante in licitantes:
    subset = df_filtrado[df_filtrado["Licitante"] == licitante]  # Filtrar os dados do licitante
    plt.step(
        subset["Data/Hora"],
        subset["Valor"],
        where="post",  # Ajuste para melhor visualização
        linewidth=1,  # Linhas mais finas
        label=licitante
    )

# Configurações do gráfico
plt.xlabel("Data/Hora")
plt.ylabel("Valor do Lance (R$)")
plt.title("Evolução dos Lances ao Longo do Tempo")
plt.xticks(rotation=60)  # Ajusta a rotação das datas no eixo X

# Definir o limite superior do eixo Y para evitar achatamento
#plt.yscale("log")
plt.ylim(limite_inferior, limite_superior)

# Formatar os valores do eixo Y como reais (R$)
plt.gca().yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'R$ {x:,.2f}'))

# Adicionar a legenda dentro do gráfico
plt.legend(
    title="Licitante",
    loc="upper right",   # Posiciona no canto superior direito dentro do gráfico
    bbox_to_anchor=(1, 1),  # Pequeno deslocamento interno
    facecolor="white",  # Fundo branco para melhor legibilidade
    edgecolor="black",  # Borda preta
    fontsize=10,        # Tamanho da fonte ajustado
    framealpha=0.8      # Transparência para não cobrir os dados completamente
)

# Melhorar a distribuição dos dados
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

# Ajustar layout para melhor visualização
plt.tight_layout()

# Mostrar o gráfico ajustado
plt.show()