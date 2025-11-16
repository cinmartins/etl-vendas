# Pipeline ETL de Vendas e Compras

Este projeto implementa pipelines ETL (Extract, Transform, Load) completos em Python para os domínios de vendas e compras de um sistema simples. O projeto segue as melhores práticas de modelagem de dados, separando dados dimensionais de dados de fatos.

## Arquitetura de Dados

A estrutura de dados foi projetada para ser escalável, com uma clara separação entre dimensões (entidades como clientes, produtos) e fatos (eventos como vendas, compras).

```
.
├── config/
│   └── config.yaml        # Arquivo de configuração do pipeline
├── data/                  # (Ignorado pelo .gitignore)
│   ├── raw/
│   │   ├── dimensao/      # Dados brutos de dimensões
│   │   ├── vendas/        # Dados brutos de fatos de vendas
│   │   └── compras/       # Dados brutos de fatos de compras
│   └── processed/
│       ├── dimensao/      # Dimensões processadas
│       ├── vendas/        # Fatos de vendas processados
│       └── compras/       # Fatos de compras processados
├── logs/                  # (Ignorado pelo .gitignore)
├── reports/               # (Ignorado pelo .gitignore)
├── src/
│   ├── etl/               # Módulos de ETL (extract, transform, load)
│   └── utils/             # Utilitários (loggers, visualizers)
├── tests/
│   ├── test_vendas_etl.py # Testes para o pipeline de vendas
│   └── test_compras_etl.py# Testes para o pipeline de compras
├── main.py                # Ponto de entrada para executar os pipelines
├── requirements.txt       # Dependências do projeto
├── .gitignore             # Arquivos e diretórios a serem ignorados pelo Git
└── README.md              # Esta documentação
```

## Configuração do Ambiente

Siga as instruções abaixo para configurar e executar o projeto localmente.

### 1. Crie um Ambiente Virtual
```bash
# Crie o ambiente virtual
python3 -m venv venv

# Ative o ambiente virtual
# No macOS e Linux:
source venv/bin/activate
```

### 2. Instale as Dependências
```bash
pip install -r requirements.txt
```

## Como Executar os Pipelines

Para executar todos os pipelines (Dimensão, Vendas e Compras) em sequência, rode o script `main.py`:

```bash
python3 main.py
```

A execução irá gerar todos os dados, relatórios e dashboards nos diretórios `data/`, `reports/` e `logs/`.

## Como Executar os Testes

Para garantir a qualidade e a corretude do código, execute a suíte de testes completa com `pytest`:

```bash
pytest
```
