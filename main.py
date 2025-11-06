from src.etl.extract import DataGenerator
from src.etl.transform import DataTransformer
from src.etl.load import DataLoader
from src.utils.data_quality import DataQuality
from src.utils.visualizer import Visualizer
from src.utils.config_loader import load_config
from src.utils.logger import logger

def main():
    """
    Orquestra a execução completa do pipeline ETL.
    """
    try:
        logger.info("Iniciando o pipeline ETL completo...")

        config = load_config()

        # Etapa de Extração
        generator = DataGenerator()
        generator.generate_all_data()

        # Etapa de Transformação
        transformer = DataTransformer()
        transformed_data = transformer.transform()

        # Etapa de Carregamento
        loader = DataLoader()
        loader.save_data(transformed_data)

        # Etapa de Qualidade de Dados
        dq_checker = DataQuality(transformed_data, config)
        dq_checker.generate_report()

        # Etapa de Visualização
        visualizer = Visualizer(transformed_data, config)
        visualizer.create_dashboard()

        logger.info("Pipeline ETL concluído com sucesso!")

    except Exception as e:
        logger.error(f"Ocorreu um erro fatal no pipeline: {e}", exc_info=True)
        # Em um cenário real, poderíamos adicionar notificações aqui (ex: email, Slack)

if __name__ == '__main__':
    main()
