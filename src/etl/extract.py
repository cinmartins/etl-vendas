import pandas as pd
import numpy as np
from faker import Faker
import os
from datetime import datetime, timedelta

from src.utils.config_loader import load_config
from src.utils.logger import logger

class DataGenerator:
    """
    Gera dados fake para clientes, produtos e vendas.
    """
    def __init__(self, config_path='config/config.yaml'):
        """
        Inicializa o gerador de dados carregando as configurações.
        """
        self.config = load_config(config_path)
        self.faker = Faker('pt_BR')
        self.vendas_raw_path = self.config['data']['vendas']['raw_path']
        self.compras_raw_path = self.config['data']['compras']['raw_path']
        os.makedirs(self.vendas_raw_path, exist_ok=True)
        os.makedirs(self.compras_raw_path, exist_ok=True)

    def generate_customers_data(self, num_records):
        """
        Gera dados de clientes.
        """
        data = []
        for i in range(num_records):
            profile = self.faker.profile()
            data.append({
                'id': i + 1,
                'nome': profile['name'],
                'email': profile['mail'],
                'telefone': self.faker.phone_number(),
                'cidade': self.faker.city(),
                'estado': self.faker.state_abbr(),
                'data_cadastro': self.faker.date_time_between(start_date='-2y', end_date='now')
            })
        return pd.DataFrame(data)

    def generate_products_data(self, num_records):
        """
        Gera dados de produtos.
        """
        categories = self.config['generator']['product_categories']
        data = []
        for i in range(num_records):
            data.append({
                'id': i + 1,
                'nome': self.faker.word().capitalize() + ' ' + self.faker.word().capitalize(),
                'categoria': np.random.choice(categories),
                'preco': round(np.random.uniform(10, 500), 2),
                'estoque': np.random.randint(0, 1000),
                'fornecedor': self.faker.company()
            })
        return pd.DataFrame(data)

    def generate_sales_data(self, num_records, customers_df, products_df):
        """
        Gera dados de vendas.
        """
        data = []
        customer_ids = customers_df['id'].tolist()
        product_ids = products_df['id'].tolist()
        for i in range(num_records):
            produto_id = np.random.choice(product_ids)
            preco_unitario = products_df.loc[products_df['id'] == produto_id, 'preco'].iloc[0]
            quantidade = np.random.randint(1, 10)
            data.append({
                'id': i + 1,
                'cliente_id': np.random.choice(customer_ids),
                'produto_id': produto_id,
                'quantidade': quantidade,
                'data_venda': self.faker.date_time_between(start_date='-1y', end_date='now'),
                'valor_total': round(preco_unitario * quantidade, 2)
            })
        return pd.DataFrame(data)

    def generate_vendas_data(self):
        """
        Orquestra a geração de dados de vendas e os salva em arquivos CSV.
        """
        logger.info("Iniciando a geração de dados de vendas...")

        num_customers = self.config['generator']['num_customers']
        customers_df = self.generate_customers_data(num_customers)
        customers_path = os.path.join(self.vendas_raw_path, self.config['data']['vendas']['customers_file'])
        customers_df.to_csv(customers_path, index=False)
        logger.info(f"{num_customers} registros de clientes gerados e salvos em '{customers_path}'")

        num_products = self.config['generator']['num_products']
        products_df = self.generate_products_data(num_products)
        products_path = os.path.join(self.vendas_raw_path, self.config['data']['vendas']['products_file'])
        products_df.to_csv(products_path, index=False)
        logger.info(f"{num_products} registros de produtos gerados e salvos em '{products_path}'")

        num_sales = self.config['generator']['num_sales']
        sales_df = self.generate_sales_data(num_sales, customers_df, products_df)
        sales_path = os.path.join(self.vendas_raw_path, self.config['data']['vendas']['sales_file'])
        sales_df.to_csv(sales_path, index=False)
        logger.info(f"{num_sales} registros de vendas gerados e salvos em '{sales_path}'")

        logger.info("Geração de dados de vendas concluída.")
        return customers_df, products_df, sales_df

    def generate_compras_data(self, products_df):
        """
        Gera dados de compras de produtos e os salva em um arquivo CSV.
        """
        logger.info("Iniciando a geração de dados de compras...")
        num_purchases = self.config['generator']['num_purchases']
        product_ids = products_df['id'].tolist()
        data = []
        for i in range(num_purchases):
            quantidade = np.random.randint(10, 100)
            custo_unitario = round(np.random.uniform(5, 400), 2)
            data.append({
                'id': i + 1,
                'produto_id': np.random.choice(product_ids),
                'quantidade': quantidade,
                'data_compra': self.faker.date_time_between(start_date='-1y', end_date='now'),
                'custo_total': round(custo_unitario * quantidade, 2)
            })

        purchases_df = pd.DataFrame(data)
        purchases_path = os.path.join(self.compras_raw_path, self.config['data']['compras']['purchases_file'])
        purchases_df.to_csv(purchases_path, index=False)
        logger.info(f"{num_purchases} registros de compras gerados e salvos em '{purchases_path}'")
        return purchases_df

if __name__ == '__main__':
    generator = DataGenerator()
    customers, products, sales = generator.generate_vendas_data()
    generator.generate_compras_data(products)
