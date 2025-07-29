import matplotlib.pyplot as plt

def plot_equity_curve(df, output_path='../plots/equity_curve.png'):
    plt.figure(figsize=(10, 5))
    plt.plot(df['Equity_Curve'], label='Strategy Equity Curve')
    plt.title("Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_comparison_equity_curves(results_dict: dict, output_path='../plots/equity_comparison.png'):
    """
    Plots equity curves from multiple result DataFrames.
    Expects: {'Label': DataFrame, ...}
    """
    plt.figure(figsize=(12, 6))
    for label, df in results_dict.items():
        plt.plot(df['Equity_Curve'], label=label)
    plt.title("Equity Curve Comparison")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
