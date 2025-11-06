import os
import pandas as pd

from src.utils.config_loader import load_config
from src.etl.transform import DataTransformer
from src.utils.logger import logger

class DataLoader:
    """
    Carrega os dados transformados em diferentes formatos (CSV, JSON, Parquet).
    """
    def __init__(self, config_path='config/config.yaml'):
        """
        Inicializa o carregador de dados.
        """
        self.config = load_config(config_path)
        self.vendas_processed_path = self.config['data']['vendas']['processed_path']
        self.compras_processed_path = self.config['data']['compras']['processed_path']
        os.makedirs(self.vendas_processed_path, exist_ok=True)
        os.makedirs(self.compras_processed_path, exist_ok=True)

    def save_vendas_data(self, data_dict):
        """
        Salva os DataFrames de vendas em formato Parquet.

        Args:
            data_dict (dict): Um dicionário de DataFrames a serem salvos.
        """
        logger.info("Iniciando a fase de carregamento de dados de vendas...")
        for name, df in data_dict.items():
            base_path = os.path.join(self.vendas_processed_path, name)

            # Salvar em Parquet
            parquet_path = f"{base_path}.parquet"
            df.to_parquet(parquet_path, index=False)

            logger.info(f"Dados de '{name}' de vendas salvos em formato Parquet.")
        logger.info("Carregamento de dados de vendas concluído.")

    def save_compras_data(self, data_dict):
        """
        Salva os DataFrames de compras em formato Parquet.

        Args:
            data_dict (dict): Um dicionário de DataFrames a serem salvos.
        """
        logger.info("Iniciando a fase de carregamento de dados de compras...")
        for name, df in data_dict.items():
            base_path = os.path.join(self.compras_processed_path, name)

            # Salvar em Parquet
            parquet_path = f"{base_path}.parquet"
            df.to_parquet(parquet_path, index=False)

            logger.info(f"Dados de '{name}' de compras salvos em formato Parquet.")
        logger.info("Carregamento de dados de compras concluído.")

if __name__ == '__main__':
    # Este script agora é destinado a ser chamado a partir do main.py
    pass
