import pandas as pd
import os

from src.utils.config_loader import load_config
from src.utils.logger import logger

class ComprasDataTransformer:
    """
    Transforma os dados brutos de compras, aplicando limpeza, cálculos e agregações.
    """
    def __init__(self, products_df, config_path='config/config.yaml'):
        """
        Inicializa o transformador de dados de compras.
        """
        self.config = load_config(config_path)
        self.compras_raw_path = self.config['data']['compras']['raw_path']
        self.products_df = products_df # Recebe o DF de produtos para joins

    def _read_data(self):
        """
        Lê os dados brutos de compras do diretório.
        """
        try:
            purchases_path = os.path.join(self.compras_raw_path, self.config['data']['compras']['purchases_file'])
            self.purchases_df = pd.read_csv(purchases_path)
            logger.info("Dados brutos de compras lidos com sucesso.")
        except FileNotFoundError as e:
            logger.error(f"Erro: Arquivo de compras não encontrado - {e}")
            raise

    def _clean_data(self):
        """
        Limpa os dados, tratando valores nulos e duplicatas.
        """
        self.purchases_df.dropna(inplace=True)
        self.purchases_df.drop_duplicates(subset=['id'], inplace=True)
        logger.info("Limpeza de dados de compras (nulos e duplicatas) concluída.")

    def _validate_data_types(self):
        """
        Valida e converte os tipos de dados.
        """
        self.purchases_df['data_compra'] = pd.to_datetime(self.purchases_df['data_compra'])
        self.purchases_df['custo_total'] = pd.to_numeric(self.purchases_df['custo_total'])
        logger.info("Tipos de dados de compras validados e convertidos.")

    def _aggregate_data(self):
        """
        Realiza agregações nos dados de compras.
        """
        # Compras mensais
        self.purchases_df['mes_compra'] = self.purchases_df['data_compra'].dt.to_period('M').astype(str)
        self.monthly_purchases = self.purchases_df.groupby('mes_compra').agg(
            custo_total=('custo_total', 'sum'),
            quantidade_total=('quantidade', 'sum')
        ).reset_index()

        # Custo por fornecedor
        purchases_with_supplier = pd.merge(self.purchases_df, self.products_df[['id', 'fornecedor']], left_on='produto_id', right_on='id')
        self.cost_by_supplier = purchases_with_supplier.groupby('fornecedor').agg(
            custo_total=('custo_total', 'sum')
        ).nlargest(10, 'custo_total').reset_index()

        logger.info("Agregação de dados de compras (compras mensais, custo por fornecedor) concluída.")

    def transform(self):
        """
        Orquestra todo o processo de transformação de compras.
        """
        logger.info("Iniciando a fase de transformação de dados de compras...")
        self._read_data()
        self._clean_data()
        self._validate_data_types()
        self._aggregate_data()
        logger.info("Transformação de dados de compras concluída.")

        return {
            "compras": self.purchases_df,
            "compras_mensais": self.monthly_purchases,
            "custo_por_fornecedor": self.cost_by_supplier
        }

if __name__ == '__main__':
    config = load_config()
    products_path = os.path.join(config['data']['vendas']['raw_path'], config['data']['vendas']['products_file'])
    products_df = pd.read_csv(products_path)

    compras_transformer = ComprasDataTransformer(products_df)
    transformed_compras_data = compras_transformer.transform()

    for name, df in transformed_compras_data.items():
        print(f"\n--- {name.replace('_', ' ').title()} ---")
        print(df.head())
