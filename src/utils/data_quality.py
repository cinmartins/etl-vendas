import pandas as pd
import os

class DataQuality:
    """
    Gera um relatório de qualidade de dados para múltiplos domínios.
    """
    def __init__(self, config):
        """
        Inicializa o verificador de qualidade de dados.
        """
        self.config = config
        self.reports_path = self.config['data']['reports_path']
        os.makedirs(self.reports_path, exist_ok=True)
        self.report_content = ""

    def check(self, data_dict, domain_name):
        """
        Verifica a qualidade de um dicionário de dados e adiciona ao relatório.
        """
        self.report_content += f"\n{'='*20} DOMÍNIO: {domain_name.upper()} {'='*20}\n"
        for name, df in data_dict.items():
            self.report_content += f"\n--- Análise de Qualidade para '{name}' ---\n"
            self.report_content += f"Dimensões: {df.shape[0]} linhas, {df.shape[1]} colunas\n"

            # Checagem de nulos
            null_counts = df.isnull().sum()
            self.report_content += f"Valores Nulos por Coluna:\n{null_counts[null_counts > 0].to_string()}\n\n"

            # Checagem de duplicatas
            num_duplicates = df.duplicated().sum()
            self.report_content += f"Número de Linhas Duplicadas: {num_duplicates}\n\n"

            # Estatísticas descritivas
            self.report_content += f"Estatísticas Descritivas:\n{df.describe().to_string()}\n"
            self.report_content += "-"*50 + "\n"

    def save_report(self):
        """
        Salva o relatório de qualidade de dados acumulado.
        """
        print("\nSalvando relatório de qualidade de dados...")
        report_path = os.path.join(self.reports_path, "data_quality_report.txt")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(self.report_content)
        print(f"Relatório de qualidade de dados salvo em '{report_path}'")
