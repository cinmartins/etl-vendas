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
        self.processed_path = self.config['data']['processed_path']
        os.makedirs(self.processed_path, exist_ok=True)

    def save_data(self, data_dict):
        """
        Salva os DataFrames em múltiplos formatos.

        Args:
            data_dict (dict): Um dicionário de DataFrames a serem salvos.
        """
        logger.info("Iniciando a fase de carregamento de dados...")
        for name, df in data_dict.items():
            base_path = os.path.join(self.processed_path, name)

            # Salvar em Parquet
            parquet_path = f"{base_path}.parquet"
            df.to_parquet(parquet_path, index=False)

            logger.info(f"Dados de '{name}' salvos em formato Parquet.")
        logger.info("Carregamento de dados concluído.")

if __name__ == '__main__':
    # Executa a transformação para obter os dados
    transformer = DataTransformer()
    transformed_data = transformer.transform()

    # Executa o carregamento dos dados transformados
    loader = DataLoader()
    loader.save_data(transformed_data)
