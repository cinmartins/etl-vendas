import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

class Visualizer:
    """
    Cria visualizações a partir dos dados transformados com foco em storytelling.
    """
    def __init__(self, data_dict, config):
        """
        Inicializa o visualizador.
        """
        self.data_dict = data_dict
        self.reports_path = config['data']['reports_path']
        os.makedirs(self.reports_path, exist_ok=True)
        # Estilo mais limpo e profissional
        sns.set_theme(style="whitegrid", palette="viridis")

    def _add_data_labels(self, ax, is_barh=True):
        """Adiciona rótulos de dados a um gráfico."""
        for p in ax.patches:
            if is_barh:
                width = p.get_width()
                ax.text(width + 0.1, p.get_y() + p.get_height() / 2.,
                        f'R$ {width:,.0f}'.replace(',', '.'),
                        va='center')
            else: # bar vertical
                height = p.get_height()
                ax.text(p.get_x() + p.get_width() / 2., height + 3,
                        f'R$ {height:,.0f}'.replace(',', '.'),
                        ha='center')

    def create_dashboard(self):
        """
        Cria e salva um dashboard com múltiplos gráficos otimizados.
        """
        print("\nGerando dashboard de visualização aprimorado...")

        fig, axes = plt.subplots(3, 1, figsize=(14, 22))
        fig.suptitle('Análise de Performance de Vendas', fontsize=20, weight='bold')

        # --- Gráfico 1: Vendas por Categoria ---
        sales_by_category_df = self.data_dict['vendas_por_categoria'].sort_values('valor_total', ascending=False)
        ax1 = sns.barplot(ax=axes[0], x='valor_total', y='categoria', data=sales_by_category_df, orient='h')
        axes[0].set_title('Categorias de Produtos com Maior Volume de Vendas', fontsize=16, pad=20)
        axes[0].set_xlabel('Valor Total de Vendas (R$)', fontsize=12)
        axes[0].set_ylabel('Categoria', fontsize=12)
        axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R$ {int(x/1000)}k'))
        self._add_data_labels(axes[0])
        sns.despine(ax=axes[0])

        # --- Gráfico 2: Top 10 Clientes ---
        top_customers_df = self.data_dict['top_clientes'].sort_values('valor_total', ascending=False)
        ax2 = sns.barplot(ax=axes[1], x='valor_total', y='nome', data=top_customers_df, orient='h')
        axes[1].set_title('Top 10 Clientes por Valor de Compra', fontsize=16, pad=20)
        axes[1].set_xlabel('Valor Total de Vendas (R$)', fontsize=12)
        axes[1].set_ylabel('Cliente', fontsize=12)
        axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R$ {int(x/1000)}k'))
        self._add_data_labels(axes[1])
        sns.despine(ax=axes[1])

        # --- Gráfico 3: Vendas Mensais ---
        monthly_sales_df = self.data_dict['vendas_mensais'].copy()
        monthly_sales_df['mes_venda'] = pd.to_datetime(monthly_sales_df['mes_venda'])
        monthly_sales_df = monthly_sales_df.sort_values('mes_venda')

        axes[2].plot(monthly_sales_df['mes_venda'], monthly_sales_df['valor_total'], marker='o', linestyle='-', color=sns.color_palette("viridis")[3])
        axes[2].set_title('Evolução das Vendas ao Longo do Tempo', fontsize=16, pad=20)
        axes[2].set_xlabel('Mês da Venda', fontsize=12)
        axes[2].set_ylabel('Valor Total de Vendas (R$)', fontsize=12)
        axes[2].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R$ {int(x/1000)}k'))
        axes[2].tick_params(axis='x', rotation=45)
        sns.despine(ax=axes[2])
        axes[2].grid(axis='x', linestyle='--', alpha=0.6)

        plt.tight_layout(rect=[0, 0, 1, 0.96])

        dashboard_path = os.path.join(self.reports_path, "sales_dashboard.png")
        plt.savefig(dashboard_path, dpi=150) # Aumentar a resolução
        print(f"Dashboard aprimorado salvo em '{dashboard_path}'")
        plt.close()
