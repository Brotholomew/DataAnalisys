import math

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from pyparsing import col

AppleReleaseDates = ["2011-10", "2012-09", "2013-09", "2014-09", "2015-09", "2016-09", "2017-09", "2018-09", "2019-09", "2020-09", "2021-09"]
AndroidReleaseDates = ["2010-12", "2011-02", "2013-10", "2014-11", "2015-10", "2016-08", "2017-08", "2018-08", "2019-09", "2020-07", "2021-10"]
WindowsReleaseDates = ["2012-10", "2013-02", "2014-04", "2015-10", "2016-03", "2017-05"]

def get_year(date):
    return date.split("-")[0]

def get_month(date):
    return date.split("-")[1]

def get_year_month(date):
    return date.split("-")[0] + "-" + date.split("-")[1]

def posts_by_months(PostsDF):
    # Create column with year and month
    PostsDF['YearMonth'] = PostsDF['creationDate'].apply(lambda date: get_year_month(date))
    
    # Count created posts for each year and month
    postsByMonths = PostsDF.groupby('YearMonth')['id'].count().reset_index(name = 'Count')

    return postsByMonths

def prices_by_months(PricesDF):
    PricesDF['YearMonth'] = PricesDF['DATE'].apply(lambda date: get_year_month(date))
    PricesDF['Price'] = pd.to_numeric(PricesDF['Price'], errors='coerce')

    pricesByMonths = PricesDF.groupby('YearMonth')['Price'].mean().reset_index(name = 'Count')
    return pricesByMonths

def draw_plot_post_by_months(Data, ServiceName):
    # Plot line
    plt.figure(dpi=1200)
    plt.plot(Data['YearMonth'], Data['Posts'], color = 'purple')
    plt.plot(Data['YearMonth'], Data['Price'], color = 'green')

    maxMonths = 30

    # Generate labels
    plt.xticks(range(0, len(Data['YearMonth']), math.floor(len(Data['YearMonth']) / (maxMonths - 1))), rotation = 90)
    plt.title(f"Liczba wpisów dla poszczególnych miesięcy w serwisie {ServiceName}")
    plt.ylabel("Liczba utworzonych wpisów")

    # Save to file
    plt.autoscale()
    plt.savefig(f"{ServiceName}_posts_by_months.png", bbox_inches = "tight")

def crypto_showcase(data_repository):
    # Import sets as Pandas DataFrames
    Bitcoin_PostsDF = pd.DataFrame([vars(post) for post in data_repository.data_sets[5].posts])
    #Apple_VotesDF = pd.DataFrame([vars(vote) for vote in data_repository.data_sets[2].votes])

    Ethereum_PostsDF = pd.DataFrame([vars(post) for post in data_repository.data_sets[6].posts])
    # Apple_VotesDF = pd.DataFrame([vars(vote) for vote in data_repository.data_sets[2].votes])

    # Number of new posts for each month and year
    Bitcoin_PostsByMonths = posts_by_months(Bitcoin_PostsDF)
    Ethereum_PostsByMonths = posts_by_months(Ethereum_PostsDF)

    BitcoinPriceHistory = pd.read_csv('CBBTCUSD.csv').rename(columns={'CBBTCUSD':'Price'})
    BitcoinPriceByMonths = prices_by_months(BitcoinPriceHistory)

    EthereumPriceHistory = pd.read_csv('CBETHUSD.csv').rename(columns={'CBETHUSD':'Price'})
    EthereumPriceByMonths = prices_by_months(EthereumPriceHistory)

    # Merge data sets
    BitcoinData = pd.merge(Bitcoin_PostsByMonths, BitcoinPriceByMonths, on = 'YearMonth', how = 'inner').fillna(0)
    BitcoinData.columns = ['YearMonth', 'Posts', 'Price']
    BitcoinData['Price'] = BitcoinData['Price'].apply(lambda x: x / 10)

    # Merge data sets
    EthereumData = pd.merge(Ethereum_PostsByMonths, EthereumPriceByMonths, on='YearMonth', how='inner').fillna(0)
    EthereumData.columns = ['YearMonth', 'Posts', 'Price']

    # Draw plots
    draw_plot_post_by_months(BitcoinData, "BitcoinPrice")
    draw_plot_post_by_months(EthereumData, "Ethereum")
    #draw_plot_post_by_months(data, "BitcoinPosts", "Bitcoin", "purple")
    #draw_plot_post_by_months(Ethereum_PostsByMonths, "Count", "Ethereum", "green")

