# Pipeline ETL de Vendas

Este projeto implementa um pipeline ETL (Extract, Transform, Load) completo em Python para um sistema de vendas simples. O pipeline gera dados fake, realiza transformações robustas e salva os dados processados em múltiplos formatos, além de gerar relatórios de qualidade e visualizações.

## Estrutura do Projeto

A estrutura do projeto foi projetada para ser modular e escalável:

```
.
├── config/
│   └── config.yaml        # Arquivo de configuração do pipeline
├── data/
│   ├── raw/               # Dados brutos gerados pela extração
│   └── processed/         # Dados limpos e transformados
├── logs/
│   └── etl_pipeline.log   # Logs de execução do pipeline
├── reports/
│   ├── data_quality_report.txt # Relatório de qualidade dos dados
│   └── sales_dashboard.png     # Dashboard com visualizações
├── src/
│   ├── etl/               # Módulos principais do ETL (extract, transform, load)
│   ├── utils/             # Utilitários (logger, config, etc.)
│   └── __init__.py
├── tests/
│   └── test_etl.py        # Testes unitários do pipeline
├── main.py                # Ponto de entrada para executar o pipeline
├── requirements.txt       # Dependências do projeto
└── README.md              # Esta documentação
```

## Configuração do Ambiente

Siga as instruções abaixo para configurar e executar o projeto localmente.

### 1. Crie um Ambiente Virtual

É uma boa prática usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Crie o ambiente virtual
python3 -m venv venv

# Ative o ambiente virtual
# No macOS e Linux:
source venv/bin/activate
# No Windows:
# venv\Scripts\activate
```

### 2. Instale as Dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias a partir do arquivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

## Como Executar o Pipeline

Para executar o pipeline completo de ponta a ponta, basta rodar o script `main.py` a partir da raiz do projeto:

```bash
python3 main.py
```

A execução do script irá realizar as seguintes etapas:
1.  **Extração**: Gera dados fake de clientes, produtos e vendas e os salva em `data/raw/`.
2.  **Transformação**: Limpa, valida, enriquece e agrega os dados brutos.
3.  **Carga**: Salva os dados processados e agregados em `data/processed/` no formato Parquet.
4.  **Relatórios**: Gera um relatório de qualidade em `reports/data_quality_report.txt` e um dashboard visual em `reports/sales_dashboard.png`.
5.  **Logging**: Registra todas as operações no arquivo `logs/etl_pipeline.log`.

## Como Executar os Testes

Para garantir a qualidade e a corretude do código, você pode executar a suíte de testes unitários com o `pytest`:

```bash
pytest
```
