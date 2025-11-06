import pytest
import pandas as pd
import os

from src.etl.extract import DataGenerator
from src.etl.transform_compras import ComprasDataTransformer
from src.utils.config_loader import load_config

@pytest.fixture(scope='module')
def config():
    """Fixture para carregar a configuração."""
    return load_config()

@pytest.fixture(scope='module')
def products_df():
    """Fixture para gerar dados de produtos para os testes."""
    generator = DataGenerator()
    _, products, _ = generator.generate_vendas_data()
    return products

def test_compras_data_generation(products_df, config):
    """Testa se a geração de dados de compras cria o número esperado de registros."""
    generator = DataGenerator()
    compras_df = generator.generate_compras_data(products_df)
    num_purchases = config['generator']['num_purchases']

    assert len(compras_df) == num_purchases
    assert os.path.exists(os.path.join(config['data']['compras']['raw_path'], config['data']['compras']['purchases_file']))

def test_compras_data_transformation(products_df, config):
    """Testa a lógica de transformação de compras."""
    # Garante que os dados brutos de compras existam
    if not os.path.exists(os.path.join(config['data']['compras']['raw_path'], config['data']['compras']['purchases_file'])):
        pytest.skip("Dados brutos de compras não encontrados, pulando teste de transformação.")

    compras_transformer = ComprasDataTransformer(products_df)
    transformed_data = compras_transformer.transform()

    assert "compras_mensais" in transformed_data
    assert "custo_por_fornecedor" in transformed_data
    assert not transformed_data["compras"].isnull().values.any()
    assert len(transformed_data["custo_por_fornecedor"]) <= 10
