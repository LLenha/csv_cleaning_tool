import os
import glob
import pandas as pd

# Pastas
pasta_sischef = r"C:/Users/Samsung/Desktop/Jobs/Base - Analise/Base_Sischef"
pasta_saida = r"C:/Users/Samsung/Desktop/Jobs/Base - Analise/Base_Python_Sischef"

os.makedirs(pasta_saida, exist_ok=True)


def extrair_loja(caminho_arquivo):
    # Extrai nome da loja do arquivo: pedidos_<loja>_... → <loja>
    nome = os.path.basename(caminho_arquivo)
    partes = nome.split('_')
    return partes[1] if len(partes) > 1 else 'desconhecida'


# --- PEDIDOS ---
arquivos_pedidos = glob.glob(os.path.join(pasta_sischef, 'pedidos_*.xls'))
pedidos_por_loja = {}

# Agrupar pedidos por loja
for arquivo in arquivos_pedidos:
    loja = extrair_loja(arquivo)
    df = pd.read_excel(arquivo)
    
    if loja not in pedidos_por_loja:
        pedidos_por_loja[loja] = []
    pedidos_por_loja[loja].append(df)

# Salvar pedidos agrupados por loja
for loja, lista_dfs in pedidos_por_loja.items():
    df_final = pd.concat(lista_dfs, ignore_index=True)
    # Adicionar coluna Loja
    df_final['Loja'] = loja
    # Salvar CSV
    caminho_saida = os.path.join(pasta_saida, f'pedidos_{loja}_geral.csv')
    df_final.to_csv(caminho_saida, index=False, encoding='utf-8')

# --- PRODUTOS ---
arquivos_produtos = glob.glob(os.path.join(pasta_sischef, 'produtos_*.xls'))
produtos_por_loja = {}

# Agrupar produtos por loja
for arquivo in arquivos_produtos:
    loja = extrair_loja(arquivo)
    df = pd.read_excel(arquivo)
    
    # Filtrar apenas COMPOSICAO == 'NÃO'
    if 'COMPOSICAO' in df.columns:
        df = df[df['COMPOSICAO'] == 'NÃO']
    
    if loja not in produtos_por_loja:
        produtos_por_loja[loja] = []
    produtos_por_loja[loja].append(df)

# Salvar produtos agrupados por loja
for loja, lista_dfs in produtos_por_loja.items():
    df_final = pd.concat(lista_dfs, ignore_index=True)
    # Adicionar coluna Loja
    df_final['Loja'] = loja
    # Salvar CSV
    caminho_saida = os.path.join(pasta_saida, f'produtos_{loja}_geral.csv')
    df_final.to_csv(caminho_saida, index=False, encoding='utf-8')
