import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class Visualizer:
    """
    Cria visualizações minimalistas a partir dos dados transformados.
    """
    def __init__(self, data_dict, config):
        """
        Inicializa o visualizador.
        """
        self.data_dict = data_dict
        self.reports_path = config['data']['reports_path']
        os.makedirs(self.reports_path, exist_ok=True)
        # Estilo minimalista, sem grades
        sns.set_theme(style="white", palette="viridis")

    def create_dashboard(self):
        """
        Cria e salva um dashboard com um design limpo e focado.
        """
        print("\nGerando dashboard minimalista final...")

        fig, axes = plt.subplots(4, 1, figsize=(12, 24))
        fig.suptitle('Análise de Performance de Vendas', fontsize=20, weight='bold', y=0.98)

        # --- Gráfico 1: Vendas por Categoria ---
        sales_by_category_df = self.data_dict['vendas_por_categoria'].sort_values('valor_total', ascending=False)
        sns.barplot(ax=axes[0], x='valor_total', y='categoria', data=sales_by_category_df, orient='h')
        axes[0].set_title('Categorias com Maior Volume de Vendas', fontsize=16, pad=20)
        axes[0].set_xlabel('')
        axes[0].set_ylabel('')
        axes[0].set_xticks([])
        sns.despine(ax=axes[0], left=True, bottom=True)

        # --- Gráfico 2: Top 10 Clientes ---
        top_customers_df = self.data_dict['top_clientes'].sort_values('valor_total', ascending=False)
        sns.barplot(ax=axes[1], x='valor_total', y='nome', data=top_customers_df, orient='h')
        axes[1].set_title('Top 10 Clientes por Valor de Compra', fontsize=16, pad=20)
        axes[1].set_xlabel('')
        axes[1].set_ylabel('')
        axes[1].set_xticks([])
        sns.despine(ax=axes[1], left=True, bottom=True)

        # --- Gráfico 3: Vendas Mensais ---
        monthly_sales_df = self.data_dict['vendas_mensais'].copy()
        monthly_sales_df['mes_venda'] = pd.to_datetime(monthly_sales_df['mes_venda'])
        monthly_sales_df = monthly_sales_df.sort_values('mes_venda')

        axes[2].plot(monthly_sales_df['mes_venda'], monthly_sales_df['valor_total'], marker='o', linestyle='-', color=sns.color_palette("viridis")[3])
        axes[2].set_title('Evolução das Vendas ao Longo do Tempo', fontsize=16, pad=20)
        axes[2].set_xlabel('')
        axes[2].set_ylabel('')
        axes[2].tick_params(axis='x', rotation=45)
        axes[2].set_yticks([])
        sns.despine(ax=axes[2], left=True, bottom=True)

        # --- Gráfico 4: Top 5 Produtos do Último Mês ---
        top_products_df = self.data_dict['produtos_mais_vendidos_por_mes']
        last_month = top_products_df['mes_venda'].max()
        top_5_last_month = top_products_df[top_products_df['mes_venda'] == last_month].head(5)

        sns.barplot(ax=axes[3], x='quantidade_total', y='nome', data=top_5_last_month, orient='h')
        axes[3].set_title(f'Top 5 Produtos Mais Vendidos em {last_month}', fontsize=16, pad=20)
        axes[3].set_xlabel('')
        axes[3].set_ylabel('')
        axes[3].set_xticks([])
        sns.despine(ax=axes[3], left=True, bottom=True)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        dashboard_path = os.path.join(self.reports_path, "sales_dashboard.png")
        plt.savefig(dashboard_path, dpi=150)
        print(f"Dashboard minimalista final salvo em '{dashboard_path}'")
        plt.close()
