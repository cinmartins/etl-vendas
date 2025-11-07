import pandas as pd
import numpy as np
import os

from src.utils.config_loader import load_config
from src.utils.logger import logger

class DataTransformer:
    """
    Transforma os dados brutos, aplicando limpeza, cálculos e agregações.
    """
    def __init__(self, config_path='config/config.yaml'):
        """
        Inicializa o transformador de dados.
        """
        self.config = load_config(config_path)
        self.dimensao_raw_path = self.config['data']['dimensao']['raw_path']
        self.vendas_raw_path = self.config['data']['vendas']['raw_path']
        self.profit_margin_rate = self.config['transformation']['profit_margin_rate']

    def _read_data(self):
        """
        Lê os dados brutos dimensionais e de vendas.
        """
        try:
            customers_path = os.path.join(self.dimensao_raw_path, self.config['data']['dimensao']['customers_file'])
            self.customers_df = pd.read_csv(customers_path)

            products_path = os.path.join(self.dimensao_raw_path, self.config['data']['dimensao']['products_file'])
            self.products_df = pd.read_csv(products_path)

            sales_path = os.path.join(self.vendas_raw_path, self.config['data']['vendas']['sales_file'])
            self.sales_df = pd.read_csv(sales_path)
            logger.info("Dados brutos (dimensões e vendas) lidos com sucesso.")
        except FileNotFoundError as e:
            logger.error(f"Erro: Arquivo não encontrado - {e}")
            raise

    def _clean_data(self):
        """
        Limpa os dados, tratando valores nulos e duplicatas.
        """
        self.customers_df.dropna(inplace=True)
        self.customers_df.drop_duplicates(subset=['id'], inplace=True)

        self.products_df.dropna(inplace=True)
        self.products_df.drop_duplicates(subset=['id'], inplace=True)

        self.sales_df.dropna(inplace=True)
        self.sales_df.drop_duplicates(subset=['id'], inplace=True)
        logger.info("Limpeza de dados (nulos e duplicatas) concluída.")

    def _validate_data_types(self):
        """
        Valida e converte os tipos de dados.
        """
        self.customers_df['data_cadastro'] = pd.to_datetime(self.customers_df['data_cadastro'])
        self.sales_df['data_venda'] = pd.to_datetime(self.sales_df['data_venda'])

        self.products_df['preco'] = pd.to_numeric(self.products_df['preco'])
        self.sales_df['valor_total'] = pd.to_numeric(self.sales_df['valor_total'])
        logger.info("Tipos de dados validados e convertidos.")

    def _enrich_data(self):
        """
        Cria novas colunas e realiza cálculos.
        """
        # Recalcula o valor_total para garantir consistência
        sales_with_price = pd.merge(self.sales_df, self.products_df[['id', 'preco']], left_on='produto_id', right_on='id', how='left')
        sales_with_price['valor_total'] = sales_with_price['quantidade'] * sales_with_price['preco']
        self.sales_df = sales_with_price.drop(columns=['id_y', 'preco']).rename(columns={'id_x': 'id'})

        # Calcula a margem de lucro
        self.sales_df['margem_lucro'] = self.sales_df['valor_total'] * self.profit_margin_rate
        logger.info("Enriquecimento de dados (cálculo de margem de lucro) concluído.")

    def _aggregate_data(self):
        """
        Realiza agregações nos dados.
        """
        # Vendas por categoria de produto
        sales_with_category = pd.merge(self.sales_df, self.products_df[['id', 'categoria']], left_on='produto_id', right_on='id')
        self.sales_by_category = sales_with_category.groupby('categoria').agg(
            valor_total=('valor_total', 'sum'),
            quantidade_total=('quantidade', 'sum')
        ).reset_index()

        # Top clientes por valor total de compras
        sales_with_customer_name = pd.merge(self.sales_df, self.customers_df[['id', 'nome']], left_on='cliente_id', right_on='id')
        self.top_customers = sales_with_customer_name.groupby('nome')['valor_total'].sum().nlargest(10).reset_index()

        # Vendas mensais
        self.sales_df['mes_venda'] = self.sales_df['data_venda'].dt.to_period('M').astype(str)
        self.monthly_sales = self.sales_df.groupby('mes_venda').agg(
            valor_total=('valor_total', 'sum'),
            quantidade_total=('quantidade', 'sum')
        ).reset_index()

        # Produtos mais vendidos por mês
        sales_with_product_name = pd.merge(self.sales_df, self.products_df[['id', 'nome']], left_on='produto_id', right_on='id')
        self.top_products_per_month = sales_with_product_name.groupby(['mes_venda', 'nome']).agg(
            quantidade_total=('quantidade', 'sum')
        ).reset_index().sort_values(['mes_venda', 'quantidade_total'], ascending=[True, False])

        logger.info("Agregação de dados (vendas por categoria, top clientes, vendas mensais, top produtos) concluída.")

    def transform(self):
        """
        Orquestra todo o processo de transformação.
        """
        logger.info("Iniciando a fase de transformação de dados...")
        self._read_data()
        self._clean_data()
        self._validate_data_types()
        self._enrich_data()
        self._aggregate_data()
        logger.info("Transformação de dados concluída.")

        return {
            "vendas": self.sales_df,
            "vendas_por_categoria": self.sales_by_category,
            "top_clientes": self.top_customers,
            "vendas_mensais": self.monthly_sales,
            "produtos_mais_vendidos_por_mes": self.top_products_per_month
        }

if __name__ == '__main__':
    transformer = DataTransformer()
    transformed_data = transformer.transform()

    # Exibe as primeiras linhas dos dataframes transformados e agregados
    for name, df in transformed_data.items():
        print(f"\n--- {name.replace('_', ' ').title()} ---")
        print(df.head())
