import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class ComprasVisualizer:
    """
    Cria visualizações minimalistas a partir dos dados de compras.
    """
    def __init__(self, data_dict, config):
        """
        Inicializa o visualizador de compras.
        """
        self.data_dict = data_dict
        self.reports_path = config['data']['reports_path']
        os.makedirs(self.reports_path, exist_ok=True)
        sns.set_theme(style="white", palette="mako")

    def create_compras_dashboard(self):
        """
        Cria e salva um dashboard de compras com um design limpo e focado.
        """
        print("\nGerando dashboard de compras...")

        fig, axes = plt.subplots(2, 1, figsize=(12, 12))
        fig.suptitle('Análise de Performance de Compras', fontsize=20, weight='bold', y=0.98)

        # --- Gráfico 1: Evolução do Custo de Compras ---
        monthly_purchases_df = self.data_dict['compras_mensais'].copy()
        monthly_purchases_df['mes_compra'] = pd.to_datetime(monthly_purchases_df['mes_compra'])
        monthly_purchases_df = monthly_purchases_df.sort_values('mes_compra')

        axes[0].plot(monthly_purchases_df['mes_compra'], monthly_purchases_df['custo_total'], marker='o', linestyle='-', color=sns.color_palette("mako")[3])
        axes[0].set_title('Evolução do Custo de Compras ao Longo do Tempo', fontsize=16, pad=20)
        axes[0].set_xlabel('')
        axes[0].set_ylabel('')
        axes[0].tick_params(axis='x', rotation=45)
        axes[0].set_yticks([])
        sns.despine(ax=axes[0], left=True, bottom=True)

        # --- Gráfico 2: Top 10 Fornecedores por Custo ---
        cost_by_supplier_df = self.data_dict['custo_por_fornecedor'].sort_values('custo_total', ascending=False)
        sns.barplot(ax=axes[1], x='custo_total', y='fornecedor', data=cost_by_supplier_df, orient='h')
        axes[1].set_title('Top 10 Fornecedores por Custo Total', fontsize=16, pad=20)
        axes[1].set_xlabel('')
        axes[1].set_ylabel('')
        axes[1].set_xticks([])
        sns.despine(ax=axes[1], left=True, bottom=True)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])

        dashboard_path = os.path.join(self.reports_path, "compras_dashboard.png")
        plt.savefig(dashboard_path, dpi=150)
        print(f"Dashboard de compras salvo em '{dashboard_path}'")
        plt.close()
