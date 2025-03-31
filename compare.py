import os
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict

# Pasta com os arquivos .xlsx
PASTA_LANCES = 'lances'

# Dicionário para armazenar os horários por lote
horarios_por_lote = {}

# Leitura dos arquivos
for i, arquivo in enumerate(sorted(os.listdir(PASTA_LANCES)), start=1):
    if arquivo.endswith('.xlsx'):
        df = pd.read_excel(os.path.join(PASTA_LANCES, arquivo), dtype=str)
        horarios = pd.to_datetime(df['Data/Hora'], format='%d/%m/%Y %H:%M:%S', errors='coerce').dropna()
        horarios_por_lote[i] = list(horarios)

# Indexação cruzada de horários com tolerância de ±1s
ocorrencias = defaultdict(set)

for lote, horarios in horarios_por_lote.items():
    for h in horarios:
        for delta in [-1, 0, 1]:
            chave = h + timedelta(seconds=delta)
            ocorrencias[chave].add(lote)

# Filtrar apenas os horários com mais de um lote
ocorrencias_multiplas = {k: v for k, v in sorted(ocorrencias.items()) if len(v) > 1}

# Impressão
for i, (momento, lotes) in enumerate(ocorrencias_multiplas.items(), start=1):
    lotes_str = ', '.join(map(str, sorted(lotes)))
    print(f"{i}. lance em {momento.strftime('%d/%m/%Y, %H:%M:%S')} - ocorreu nos lotes {lotes_str}")
