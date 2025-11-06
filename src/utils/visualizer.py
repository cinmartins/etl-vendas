import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class Visualizer:
    """
    Cria visualizações a partir dos dados transformados.
    """
    def __init__(self, data_dict, config):
        """
        Inicializa o visualizador.
        """
        self.data_dict = data_dict
        self.reports_path = config['data']['reports_path']
        os.makedirs(self.reports_path, exist_ok=True)
        sns.set(style="whitegrid")

    def create_dashboard(self):
        """
        Cria e salva um dashboard com múltiplos gráficos.
        """
        print("\nGerando dashboard de visualização...")

        fig, axes = plt.subplots(3, 1, figsize=(12, 18))
        fig.suptitle('Dashboard de Análise de Vendas', fontsize=16)

        # Gráfico 1: Vendas por Categoria
        sns.barplot(ax=axes[0], x='valor_total', y='categoria', data=self.data_dict['vendas_por_categoria'], palette='viridis')
        axes[0].set_title('Total de Vendas por Categoria')
        axes[0].set_xlabel('Valor Total (R$)')
        axes[0].set_ylabel('Categoria')

        # Gráfico 2: Top 10 Clientes
        sns.barplot(ax=axes[1], x='valor_total', y='nome', data=self.data_dict['top_clientes'], palette='plasma')
        axes[1].set_title('Top 10 Clientes por Valor de Compra')
        axes[1].set_xlabel('Valor Total (R$)')
        axes[1].set_ylabel('Cliente')

        # Gráfico 3: Vendas Mensais
        monthly_sales_df = self.data_dict['vendas_mensais'].copy()
        monthly_sales_df['mes_venda'] = pd.to_datetime(monthly_sales_df['mes_venda'])
        monthly_sales_df = monthly_sales_df.sort_values('mes_venda')
        axes[2].plot(monthly_sales_df['mes_venda'], monthly_sales_df['valor_total'], marker='o', linestyle='-')
        axes[2].set_title('Evolução das Vendas Mensais')
        axes[2].set_xlabel('Mês')
        axes[2].set_ylabel('Valor Total (R$)')
        axes[2].tick_params(axis='x', rotation=45)

        plt.tight_layout(rect=[0, 0, 1, 0.96])

        dashboard_path = os.path.join(self.reports_path, "sales_dashboard.png")
        plt.savefig(dashboard_path)
        print(f"Dashboard salvo em '{dashboard_path}'")
        plt.close()
