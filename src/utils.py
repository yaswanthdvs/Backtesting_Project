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
