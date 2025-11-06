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
        print("\nGerando dashboard minimalista...")

        fig, axes = plt.subplots(3, 1, figsize=(12, 18))
        fig.suptitle('Análise de Performance de Vendas', fontsize=20, weight='bold', y=0.98)

        # --- Gráfico 1: Vendas por Categoria ---
        sales_by_category_df = self.data_dict['vendas_por_categoria'].sort_values('valor_total', ascending=False)
        sns.barplot(ax=axes[0], x='valor_total', y='categoria', data=sales_by_category_df, orient='h')
        axes[0].set_title('Categorias com Maior Volume de Vendas', fontsize=16, pad=20)
        axes[0].set_xlabel('') # Remover label do eixo
        axes[0].set_ylabel('Categoria', fontsize=12)
        axes[0].set_xticks([]) # Remover escala de valores do eixo x
        sns.despine(ax=axes[0], left=True, bottom=True) # Remover todas as bordas

        # --- Gráfico 2: Top 10 Clientes ---
        top_customers_df = self.data_dict['top_clientes'].sort_values('valor_total', ascending=False)
        sns.barplot(ax=axes[1], x='valor_total', y='nome', data=top_customers_df, orient='h')
        axes[1].set_title('Top 10 Clientes por Valor de Compra', fontsize=16, pad=20)
        axes[1].set_xlabel('') # Remover label do eixo
        axes[1].set_ylabel('Cliente', fontsize=12)
        axes[1].set_xticks([]) # Remover escala de valores do eixo x
        sns.despine(ax=axes[1], left=True, bottom=True) # Remover todas as bordas

        # --- Gráfico 3: Vendas Mensais ---
        monthly_sales_df = self.data_dict['vendas_mensais'].copy()
        monthly_sales_df['mes_venda'] = pd.to_datetime(monthly_sales_df['mes_venda'])
        monthly_sales_df = monthly_sales_df.sort_values('mes_venda')

        axes[2].plot(monthly_sales_df['mes_venda'], monthly_sales_df['valor_total'], marker='o', linestyle='-', color=sns.color_palette("viridis")[3])
        axes[2].set_title('Evolução das Vendas ao Longo do Tempo', fontsize=16, pad=20)
        axes[2].set_xlabel('Mês da Venda', fontsize=12)
        axes[2].set_ylabel('') # Remover label do eixo
        axes[2].tick_params(axis='x', rotation=45)
        axes[2].set_yticks([]) # Remover escala de valores do eixo y
        sns.despine(ax=axes[2], left=True, bottom=True) # Remover todas as bordas

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        dashboard_path = os.path.join(self.reports_path, "sales_dashboard.png")
        plt.savefig(dashboard_path, dpi=150)
        print(f"Dashboard minimalista salvo em '{dashboard_path}'")
        plt.close()
