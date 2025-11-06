from src.etl.extract import DataGenerator
from src.etl.transform import DataTransformer
from src.etl.transform_compras import ComprasDataTransformer
from src.etl.load import DataLoader
from src.utils.data_quality import DataQuality
from src.utils.vendas_visualizer import VendasVisualizer
from src.utils.compras_visualizer import ComprasVisualizer
from src.utils.config_loader import load_config
from src.utils.logger import logger
import pandas as pd
import os

def run_vendas_pipeline(config):
    """
    Orquestra a execução completa do pipeline de Vendas.
    """
    logger.info("Iniciando o pipeline de Vendas...")

    # Etapa de Extração
    generator = DataGenerator()
    _, products_df, _ = generator.generate_vendas_data()

    # Etapa de Transformação
    transformer = DataTransformer()
    transformed_data = transformer.transform()

    # Etapa de Carregamento
    loader = DataLoader()
    loader.save_vendas_data(transformed_data)

    # Etapa de Visualização
    visualizer = VendasVisualizer(transformed_data, config)
    visualizer.create_vendas_dashboard()

    logger.info("Pipeline de Vendas concluído com sucesso!")
    return products_df, transformed_data

def run_compras_pipeline(products_df, config):
    """
    Orquestra a execução completa do pipeline de Compras.
    """
    logger.info("Iniciando o pipeline de Compras...")

    # Etapa de Extração (os dados de produtos são reutilizados)
    generator = DataGenerator()
    generator.generate_compras_data(products_df)

    # Etapa de Transformação
    compras_transformer = ComprasDataTransformer(products_df)
    transformed_data = compras_transformer.transform()

    # Etapa de Carregamento
    loader = DataLoader()
    loader.save_compras_data(transformed_data)

    # Etapa de Visualização
    visualizer = ComprasVisualizer(transformed_data, config)
    visualizer.create_compras_dashboard()

    logger.info("Pipeline de Compras concluído com sucesso!")
    return transformed_data


def main():
    """
    Ponto de entrada principal para todos os pipelines.
    """
    try:
        logger.info("Iniciando a execução do ETL...")

        config = load_config()
        dq_checker = DataQuality(config)

        products_df, vendas_data = run_vendas_pipeline(config)
        dq_checker.check(vendas_data, "Vendas")

        compras_data = run_compras_pipeline(products_df, config)
        dq_checker.check(compras_data, "Compras")

        dq_checker.save_report()

        logger.info("Execução do ETL concluída com sucesso!")

    except Exception as e:
        logger.error(f"Ocorreu um erro fatal no pipeline: {e}", exc_info=True)

if __name__ == '__main__':
    main()
