import yfinance
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

#fetch percent return over time period for each ticker passed 
def fetch_returns_matrix(tickers, period = "1y", delay_seconds = 1.0):

    price_data = {}
    for ticker in tickers:
        stock = yfinance.Ticker(ticker).history(period=period)
        price_data[ticker] = stock['Close']
        time.sleep(delay_seconds)

    prices_df = pd.DataFrame(price_data)

    returns_df = prices_df.pct_change()
    returns_df = returns_df.dropna()

    return returns_df


#create heat map of correlation matrix
def plot_correlation_heatmap(corr_matrix, title = "Correlation Matrix"):
    fig, ax = plt.subplots(figsize=(7,6))

    heatmap = ax.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
    fig.colorbar(heatmap, ax=ax)

    ax.set_xticks(range(len(corr_matrix.columns)))
    ax.set_xticklabels(corr_matrix.columns, rotation=45)
    ax.set_yticks(range(len(corr_matrix.index)))
    ax.set_yticklabels(corr_matrix.index)


    for i in range(len(corr_matrix.index)):
        for j in range(len(corr_matrix.columns)):
            value = corr_matrix.iloc[i, j]
            ax.text(j, i, f"{value:.2f}", ha="center", va="center")
    
    ax.set_title(title)
    plt.tight_layout()
    


if __name__ == "__main__":
    tickers_input = input("Enter tickers: ")
    tickers = [t.strip().upper() for t in tickers_input.split(",")]

    returns = fetch_returns_matrix(tickers)
    print(returns.shape)
    print(returns.head())

#create a covariant matrix
    print("\ncovariant matrix")
    cov_matrix = returns.cov()
    print(cov_matrix)

    cov_eigenvalues, cov_eigenvectors = np.linalg.eigh(cov_matrix)
    order = np.argsort(cov_eigenvalues)[::-1]

    sorted_cov_eigenvalues = cov_eigenvalues[order]
    sorted_cov_eigenvectors = cov_eigenvectors[:, order]

    top_cov_eigenvector = sorted_cov_eigenvectors[:, 0]

    print(sorted_cov_eigenvalues)
    print(top_cov_eigenvector)

  
#create a correlation matrix - covariant normalized with individual variance
    print("\ncorrelation matrix")
    corr_matrix = returns.corr()
    print(f"{corr_matrix}\n")

    corr_eigenvalues, corr_eigenvectors = np.linalg.eigh(corr_matrix)
    order = np.argsort(corr_eigenvalues)[::-1]

    sorted_corr_eigenvalues = corr_eigenvalues[order]
    sorted_corr_eigenvectors = corr_eigenvectors[:, order]

    top_corr_eigenvector = sorted_corr_eigenvectors[:, 0]

    
# print all eigenvectors at once, tickers as rows, PC1 as columns
    loadings_df = pd.DataFrame(
        sorted_corr_eigenvectors,
        index=corr_matrix.columns,
        columns=[f"PC{i+1}" for i in range(len(sorted_corr_eigenvalues))]
    )
    print(f"{loadings_df}\n")


#print eigenvalues, labeled by component, with variance explained
    variance_explained_pct = sorted_corr_eigenvalues / sorted_corr_eigenvalues.sum() * 100
    eigenvalue_summary = pd.DataFrame({
        "eigenvalue": sorted_corr_eigenvalues,
        "variance_explained_pct": variance_explained_pct
    }, index = [f"PC{i+1}" for i in range(len(sorted_corr_eigenvalues))])

    print(f"{eigenvalue_summary}\n")
    print(loadings_df["PC1"].sort_values())
    print("\n")
    print(loadings_df["PC2"].sort_values())
    
#show heatmap
    plot_correlation_heatmap(corr_matrix)
    plt.show()