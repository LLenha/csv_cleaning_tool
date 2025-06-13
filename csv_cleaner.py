import os
import pandas as pd

# Caminho da pasta onde estão os CSVs
pasta_produtos = "C:/Users/Samsung/Desktop/Jobs/Base - Analise/Base_Produtos"
pasta_pedidos = "C:/Users/Samsung/Desktop/Jobs/Base - Analise/Base_Pedidos"
pasta_salvar = "C:/Users/Samsung/Desktop/Jobs/Base - Analise/Base_Python"

# Padrões de agrupamento (nome das lojas)
padroes = [
    'malzoni', 'b29', 'b32', 'jkfc', 'cetenco', 'rochavera', 'riverview', 'cbre'
]

# --- PRODUTOS ---

# Lista arquivos .csv
arquivos_csv_produtos = [f for f in os.listdir(pasta_produtos) if f.endswith('.csv')]

# Dicionário para agrupar DataFrames de produtos
grupos_produtos = {f'produtos_{p}_': [] for p in padroes}

for arquivo in arquivos_csv_produtos:
    caminho_completo = os.path.join(pasta_produtos, arquivo)
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
        df_final = pd.concat(lista_dfs, ignore_index=True)
        nome_saida = f"produtos_{padrao.replace('produtos_', '').replace('_', '')}_geral.csv"
        df_final.to_csv(os.path.join(pasta_salvar, nome_saida), index=False)

# --- PEDIDOS ---

arquivos_csv_pedidos = [f for f in os.listdir(pasta_pedidos) if f.endswith('.csv')]

grupos_pedidos = {f'pedidos_{p}_': [] for p in padroes}

for arquivo in arquivos_csv_pedidos:
    caminho_completo = os.path.join(pasta_pedidos, arquivo)
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

# Salva cada grupo de pedidos em um CSV final
for padrao, lista_dfs in grupos_pedidos.items():
    if lista_dfs:
        df_final = pd.concat(lista_dfs, ignore_index=True)
        nome_saida = f"pedidos_{padrao.replace('pedidos_', '').replace('_', '')}_geral.csv"
        df_final.to_csv(os.path.join(pasta_salvar, nome_saida), index=False)

