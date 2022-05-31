import math

import pandas as pd
import matplotlib.pyplot as plt

from data_analysis.showcase.mobile_showcase import get_year_month, posts_by_months


def prices_by_months(PricesDF):
    PricesDF['YearMonth'] = PricesDF['DATE'].apply(lambda date: get_year_month(date))
    PricesDF['Price'] = pd.to_numeric(PricesDF['Price'], errors='coerce')

    pricesByMonths = PricesDF.groupby('YearMonth')['Price'].mean().reset_index(name='Count')
    return pricesByMonths


def draw_plot_post_by_months(Data, Values, Title, ServiceName):
    # Init plot
    plt.figure(dpi=1200)

    # Set plot values
    for key in Values:
        plt.plot(Data['YearMonth'], Data[key], color=Values[key]['color'], label=Values[key]['label'])

    maxMonths = 30

    # Generate labels
    plt.xticks(range(0, len(Data['YearMonth']), math.floor(len(Data['YearMonth']) / (maxMonths - 1))), rotation=90)
    plt.title(Title)

    # Save to file
    plt.legend()
    plt.autoscale()
    plt.savefig(f"{ServiceName}_posts_by_months.png", bbox_inches="tight")


def crypto_showcase(data_repository):
    # Import sets as Pandas DataFrames
    Bitcoin_PostsDF = pd.DataFrame([vars(post) for post in data_repository.data_sets[5].posts])
    Ethereum_PostsDF = pd.DataFrame([vars(post) for post in data_repository.data_sets[6].posts])

    # Number of new posts for each month and year
    Bitcoin_PostsByMonths = posts_by_months(Bitcoin_PostsDF)
    Ethereum_PostsByMonths = posts_by_months(Ethereum_PostsDF)

    # Import price history from CSV
    BitcoinPriceHistory = pd.read_csv('CBBTCUSD.csv').rename(columns={'CBBTCUSD': 'Price'})
    BitcoinPriceByMonths = prices_by_months(BitcoinPriceHistory)

    EthereumPriceHistory = pd.read_csv('CBETHUSD.csv').rename(columns={'CBETHUSD': 'Price'})
    EthereumPriceByMonths = prices_by_months(EthereumPriceHistory)

    # Merge data sets to have same data range
    BitcoinData = pd.merge(Bitcoin_PostsByMonths, BitcoinPriceByMonths, on='YearMonth', how='inner').fillna(0)
    BitcoinData.columns = ['YearMonth', 'Posts', 'Price']
    BitcoinData['PriceDivided'] = BitcoinData['Price'].apply(lambda x: x / 10)  # Some price scaling

    # Merge data sets to have same data range
    EthereumData = pd.merge(Ethereum_PostsByMonths, EthereumPriceByMonths, on='YearMonth', how='inner').fillna(0)
    EthereumData.columns = ['YearMonth', 'Posts', 'Price']

    # Draw plots - Bitcoin
    draw_plot_post_by_months(
        BitcoinData,
        {"Posts": {"color": "green", "label": "Liczba postów"}},
        "Liczba postów w serwisie Bitcoin",
        "Bitcoin_Posts"
    )
    draw_plot_post_by_months(
        BitcoinData,
        {"Price": {"color": "purple", "label": "Wartość Bitcoina [$]"}},
        "Wartość Bitcoina",
        "Bitcoin_Price"
    )
    draw_plot_post_by_months(
        BitcoinData,
        {"Posts": {"color": "green", "label": "Liczba postów"}, "PriceDivided": {"color": "purple", "label": "Wartość Bitcoina [$] (podzielona przez 10)"}},
        "Liczba postów w serwisie Bitcoin w porównaniu z wartością Bitcoina",
        "Bitcoin_Posts_Price"
    )

    # Draw plots - Ethereum
    draw_plot_post_by_months(
        EthereumData,
        {"Posts": {"color": "green", "label": "Liczba postów"}},
        "Liczba postów w serwisie Ethereum",
        "Ethereum_Posts"
    )
    draw_plot_post_by_months(
        EthereumData,
        {"Price": {"color": "purple", "label": "Wartość Ethereum [$]"}},
        "Wartość Ethereum",
        "Ethereum_Price"
    )
    draw_plot_post_by_months(
        EthereumData,
        {"Posts": {"color": "green", "label": "Liczba postów"}, "Price": {"color": "purple", "label": "Wartość Ethereum [$]"}},
        "Liczba postów w serwisie Ethereum w porównaniu z wartością Ethereum",
        "Ethereum_Posts_price"
    )
