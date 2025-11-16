import pytest
import pandas as pd
import os

from src.etl.extract import DataGenerator
from src.etl.transform import DataTransformer
from src.etl.load import DataLoader
from src.utils.config_loader import load_config

@pytest.fixture(scope='module')
def config():
    """Fixture para carregar a configuração."""
    return load_config()

@pytest.fixture(scope='module')
def dimensao_data():
    """Fixture para gerar dados dimensionais para os testes."""
    generator = DataGenerator()
    customers_df, products_df = generator.generate_dimensao_data()
    return customers_df, products_df

def test_vendas_data_generation(dimensao_data, config):
    """Testa a geração de dados de vendas."""
    customers_df, products_df = dimensao_data
    generator = DataGenerator()
    sales_df = generator.generate_vendas_data(customers_df, products_df)
    num_sales = config['generator']['num_sales']

    assert len(sales_df) == num_sales
    assert os.path.exists(os.path.join(config['data']['vendas']['raw_path'], config['data']['vendas']['sales_file']))

def test_vendas_data_transformation(config):
    """Testa a lógica de transformação de vendas."""
    if not os.path.exists(os.path.join(config['data']['vendas']['raw_path'], config['data']['vendas']['sales_file'])):
        pytest.skip("Dados brutos de vendas não encontrados.")

    transformer = DataTransformer()
    transformed_data = transformer.transform()

    assert "margem_lucro" in transformed_data["vendas"].columns
    assert not transformed_data["vendas"].isnull().values.any()

def test_vendas_data_loading(config):
    """Testa o carregamento de dados de vendas."""
    transformer = DataTransformer()
    transformed_data = transformer.transform()

    loader = DataLoader()
    loader.save_vendas_data(transformed_data)

    processed_path = config['data']['vendas']['processed_path']
    for name in transformed_data.keys():
        assert os.path.exists(os.path.join(processed_path, f"{name}.parquet"))
