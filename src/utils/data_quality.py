import pandas as pd
import os

class DataQuality:
    """
    Gera um relatório de qualidade de dados.
    """
    def __init__(self, data_dict, config):
        """
        Inicializa o verificador de qualidade de dados.
        """
        self.data_dict = data_dict
        self.reports_path = config['data']['reports_path']
        os.makedirs(self.reports_path, exist_ok=True)

    def generate_report(self):
        """
        Gera e salva o relatório de qualidade de dados.
        """
        print("\nGerando relatório de qualidade de dados...")
        report = ""
        for name, df in self.data_dict.items():
            report += f"--- Análise de Qualidade para '{name}' ---\n"
            report += f"Dimensões: {df.shape[0]} linhas, {df.shape[1]} colunas\n"

            # Checagem de nulos
            null_counts = df.isnull().sum()
            report += f"Valores Nulos por Coluna:\n{null_counts[null_counts > 0].to_string()}\n\n"

            # Checagem de duplicatas
            num_duplicates = df.duplicated().sum()
            report += f"Número de Linhas Duplicadas: {num_duplicates}\n\n"

            # Estatísticas descritivas
            report += f"Estatísticas Descritivas:\n{df.describe().to_string()}\n"
            report += "="*50 + "\n\n"

        report_path = os.path.join(self.reports_path, "data_quality_report.txt")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Relatório de qualidade de dados salvo em '{report_path}'")
