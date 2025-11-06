from src.etl.transform import DataTransformer
from src.utils.data_quality import DataQuality
from src.utils.visualizer import Visualizer
from src.utils.config_loader import load_config

def generate_reports():
    """
    Orquestra a geração de relatórios de qualidade e visualizações.
    """
    config = load_config()

    # Executa a transformação para obter os dados
    transformer = DataTransformer()
    transformed_data = transformer.transform()

    # Gera o relatório de qualidade dos dados
    dq_checker = DataQuality(transformed_data, config)
    dq_checker.generate_report()

    # Gera o dashboard de visualização
    visualizer = Visualizer(transformed_data, config)
    visualizer.create_dashboard()

if __name__ == '__main__':
    generate_reports()
