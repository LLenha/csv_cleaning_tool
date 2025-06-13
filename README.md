# CMV Agrupador de Lojas

Este projeto automatiza o processamento de arquivos CSV de produtos e pedidos de diferentes lojas. Ele realiza as seguintes tarefas:

- **Agrupa** os arquivos CSV de cada loja, tanto de produtos quanto de pedidos, em arquivos consolidados por loja.
- **Remove** colunas desnecessárias dos arquivos de pedidos.
- **Adiciona** uma coluna chamada `Loja` em cada arquivo final, identificando a qual loja os dados pertencem.
- **Gera** arquivos finais nomeados no formato `produtos_<loja>

O objetivo é facilitar a organização e análise dos dados por loja, tornando o processo mais rápido, padronizado e seguro.
