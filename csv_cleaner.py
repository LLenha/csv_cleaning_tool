import os
import glob
import pandas as pd

# Caminho da pasta onde estão os CSVs
pasta_produtos = "C:/Users/Samsung/Desktop/Jobs/Base - Analise/Base_Produtos"
pasta_pedidos = "C:/Users/Samsung/Desktop/Jobs/Base - Analise/Base_Pedidos"
pasta_salvar = "C:/Users/Samsung/Desktop/Jobs/Base - Analise/Base_Python"

# Padrões de agrupamento (nome das lojas)
padroes = [
    'malzoni', 'b29', 'b32', 'jkfc', 'cetenco', 'rochavera', 'riverview', 'cbre', 'floffice'
]


def regravar_csv(destino, dataframes):
    if os.path.exists(destino):
        os.remove(destino)

    primeiro = True
    for df in dataframes:
        df.to_csv(
            destino,
            index=False,
            mode='w' if primeiro else 'a',
            header=primeiro
        )
        primeiro = False

# --- PRODUTOS ---

# Lista arquivos .csv recursivamente (incluindo subpastas)
arquivos_csv_produtos = glob.glob(os.path.join(pasta_produtos, '**/*.csv'), recursive=True)

# Dicionário para agrupar DataFrames de produtos
grupos_produtos = {f'produtos_{p}_': [] for p in padroes}

for caminho_completo in arquivos_csv_produtos:
    arquivo = os.path.basename(caminho_completo)
    df = pd.read_csv(caminho_completo)
    for padrao in grupos_produtos.keys():
        if arquivo.startswith(padrao):
            # Adiciona a coluna Loja antes de agrupar
            loja = padrao.replace('produtos_', '').replace('_', '')
            df['Loja'] = loja
            grupos_produtos[padrao].append(df)
            break

# Salva cada grupo de produtos em um CSV final
for padrao, lista_dfs in grupos_produtos.items():
    if lista_dfs:
        nome_saida = f"produtos_{padrao.replace('produtos_', '').replace('_', '')}_geral.csv"
        caminho_saida = os.path.join(pasta_salvar, nome_saida)
        regravar_csv(caminho_saida, lista_dfs)

# --- PEDIDOS ---

# Lista arquivos .csv recursivamente (incluindo subpastas)
arquivos_csv_pedidos = glob.glob(os.path.join(pasta_pedidos, '**/*.csv'), recursive=True)

grupos_pedidos = {f'pedidos_{p}_': [] for p in padroes}

for caminho_completo in arquivos_csv_pedidos:
    arquivo = os.path.basename(caminho_completo)
    df = pd.read_csv(caminho_completo)
    # Deleta as colunas indesejadas
    colunas_para_deletar = [
        'Senha do pedido', 'CPF', 'Taxa de Serviço Na Loja (R$)', 
        'Taxa de entrega (R$)', 'Desconto (%)', 'Desconto (R$)', 
        'Desconto Fidelidade (R$)', 'Segmento do Cupom', 'Agendado', 
        'Agendado para', 'Status', 'Endereço - Logradouro', 
        'Endereço - Número', 'Endereço - Complemento', 
        'Endereço - Bairro', 'Endereço - CEP', 
        'Endereço - Cidade', 'Endereço - Estado', 
        'Endereço - Ponto de Referência', 
        'Taxa de Serviço Na Loja - Status', 'Comanda'
    ]
    df.drop(columns=colunas_para_deletar, inplace=True, errors='ignore')
    for padrao in grupos_pedidos.keys():
        if arquivo.startswith(padrao):
            loja = padrao.replace('pedidos_', '').replace('_', '')
            df['Loja'] = loja
            grupos_pedidos[padrao].append(df)
            break

# Salva cada grupo de pedidos em um CSV 
for padrao, lista_dfs in grupos_pedidos.items():
    if lista_dfs:
        nome_saida = f"pedidos_{padrao.replace('pedidos_', '').replace('_', '')}_geral.csv"
    caminho_saida = os.path.join(pasta_salvar, nome_saida)
    regravar_csv(caminho_saida, lista_dfs)

# Salva um CSV com todos os pedidos e um para todos os produtos na mesma pasta (pasta_salvar) (csvs finais)
lista_produtos_geral = [df for lista in grupos_produtos.values() for df in lista]
regravar_csv(os.path.join(pasta_salvar, "produtos_geral.csv"), lista_produtos_geral)

lista_pedidos_geral = [df for lista in grupos_pedidos.values() for df in lista]
regravar_csv(os.path.join(pasta_salvar, "pedidos_geral.csv"), lista_pedidos_geral)
