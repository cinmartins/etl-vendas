import yaml

def load_config(config_path='config/config.yaml'):
    """
    Carrega as configurações de um arquivo YAML.

    Args:
        config_path (str): O caminho para o arquivo de configuração.

    Returns:
        dict: Um dicionário com as configurações.
    """
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: O arquivo de configuração '{config_path}' não foi encontrado.")
        raise
    except Exception as e:
        print(f"Error: Erro ao carregar o arquivo de configuração: {e}")
        raise
