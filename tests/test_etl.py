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
def generated_data(config):
    """Fixture para gerar dados de teste."""
    generator = DataGenerator()
    customers_df, products_df, sales_df = generator.generate_all_data()
    return {
        "customers": customers_df,
        "products": products_df,
        "sales": sales_df
    }

def test_data_generation(generated_data, config):
    """Testa se a geração de dados cria o número esperado de registros."""
    num_customers = config['generator']['num_customers']
    num_products = config['generator']['num_products']
    num_sales = config['generator']['num_sales']

    assert len(generated_data["customers"]) == num_customers
    assert len(generated_data["products"]) == num_products
    assert len(generated_data["sales"]) == num_sales

def test_data_transformation(config):
    """Testa a lógica de transformação."""
    # Garante que os dados brutos existam
    if not os.path.exists(os.path.join(config['data']['raw_path'], config['data']['sales_file'])):
        pytest.skip("Dados brutos não encontrados, pulando teste de transformação.")

    transformer = DataTransformer()
    transformed_data = transformer.transform()

    assert "margem_lucro" in transformed_data["vendas"].columns
    assert not transformed_data["vendas"].isnull().values.any()
    assert len(transformed_data["vendas_por_categoria"]) > 0
    assert len(transformed_data["top_clientes"]) <= 10

def test_data_loading(config):
    """Testa se os arquivos de saída são criados."""
    transformer = DataTransformer()
    transformed_data = transformer.transform()

    loader = DataLoader()
    loader.save_data(transformed_data)

    processed_path = config['data']['processed_path']
    for name in transformed_data.keys():
        assert os.path.exists(os.path.join(processed_path, f"{name}.parquet"))
