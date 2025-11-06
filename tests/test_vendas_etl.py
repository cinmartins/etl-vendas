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
def generated_vendas_data(config):
    """Fixture para gerar dados de teste de vendas."""
    generator = DataGenerator()
    customers_df, products_df, sales_df = generator.generate_vendas_data()
    return {
        "customers": customers_df,
        "products": products_df,
        "sales": sales_df
    }

def test_vendas_data_generation(generated_vendas_data, config):
    """Testa se a geração de dados de vendas cria o número esperado de registros."""
    num_customers = config['generator']['num_customers']
    num_products = config['generator']['num_products']
    num_sales = config['generator']['num_sales']

    assert len(generated_vendas_data["customers"]) == num_customers
    assert len(generated_vendas_data["products"]) == num_products
    assert len(generated_vendas_data["sales"]) == num_sales

def test_vendas_data_transformation(config):
    """Testa a lógica de transformação de vendas."""
    # Garante que os dados brutos de vendas existam
    if not os.path.exists(os.path.join(config['data']['vendas']['raw_path'], config['data']['vendas']['sales_file'])):
        pytest.skip("Dados brutos de vendas não encontrados, pulando teste de transformação.")

    transformer = DataTransformer()
    transformed_data = transformer.transform()

    assert "margem_lucro" in transformed_data["vendas"].columns
    assert "produtos_mais_vendidos_por_mes" in transformed_data
    assert not transformed_data["vendas"].isnull().values.any()
    assert len(transformed_data["top_clientes"]) <= 10

def test_vendas_data_loading(config):
    """Testa se os arquivos de saída de vendas são criados."""
    transformer = DataTransformer()
    transformed_data = transformer.transform()

    loader = DataLoader()
    loader.save_vendas_data(transformed_data)

    processed_path = config['data']['vendas']['processed_path']
    for name in transformed_data.keys():
        assert os.path.exists(os.path.join(processed_path, f"{name}.parquet"))
