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

def most_popular_posts(PostsDF, VotesDF):
    # Select upvotes
    VotesDF = VotesDF[VotesDF['voteTypeId'] == 2]

    # Join posts with votes
    posts = pd.merge(PostsDF, VotesDF, how = 'inner', left_on = 'id', right_on = 'postId')

    # Count upvotes for each posts
    postUpVotes = posts.groupby(['id_x', 'title'])['id_x'].count().reset_index(name = 'UpVoteCount')

    # Sort by number of upvotes
    postUpVotes = postUpVotes.sort_values('UpVoteCount', ascending = False)

    # Get top 3 posts
    result = postUpVotes[['title', 'UpVoteCount']].head(3)

def posts_by_months(PostsDF):
    # Create column with year and month
    PostsDF['YearMonth'] = PostsDF['creationDate'].apply(lambda date: get_year_month(date))
    
    # Count created posts for each year and month
    postsByMonths = PostsDF.groupby('YearMonth')['id'].count().reset_index(name = 'Count')

    return postsByMonths

def draw_plot_post_by_months(Data, OutputPrefix, ServiceName, PointsName, PointsOfInterest, Color):
    # Generate release date markers
    markers = []
    for point in PointsOfInterest:
        rowNo = Data[Data['YearMonth'] == point].index[0]
        markers.append(rowNo)
    markerLegend = mlines.Line2D([], [], color = Color, marker = 'd', 
                        linestyle = 'None', markersize=10, label = PointsName)    

    # Plot line
    plt.figure(dpi=1200)
    plt.plot(Data['YearMonth'], Data['Count'], '-D', markevery = markers, color = Color)
    
    # Generate labels
    plt.xticks(range(0, len(Data['YearMonth']), 5), rotation = 90)
    plt.title(f"Liczby wpisów dla poszczególnych miesięcy w serwisie {ServiceName}")
    plt.ylabel("Liczba utworzonych wpisów")
    plt.legend(handles=[markerLegend])

    # Save to file
    plt.autoscale()
    plt.savefig(f"{OutputPrefix}_posts_by_months.png", bbox_inches = "tight")

def draw_plot_area(DataSets, PointsOfInterestSets, Colors, ColumnNames, MarkerNames, OutputPrefix):
    # Merge data sets
    data = DataSets[0]
    for i in range(1, len(DataSets)):
        data = pd.merge(data, DataSets[i], on = 'YearMonth', how = 'outer').fillna(0)

    # Change column names 
    data.columns = ['YearMonth'] + ColumnNames

    print(data)
    # Plot area
    plt.figure(dpi=1200)
    
    ax = data.plot.area(title = "Liczba wpisów dla poszczególnych miesięcy", ax = plt.gca(), figsize = (20, 10), rot = 90)
    ax.set_xticks(data.index, data['YearMonth'])
    ax.set_ylabel("Liczba utworzonych wpisów")

    for label in ax.xaxis.get_ticklabels()[::2]:
        label.set_visible(False)

    # Add points of interests
    markerLegend, labels = ax.get_legend_handles_labels()
    for i in range(len(PointsOfInterestSets)):
        for point in PointsOfInterestSets[i]:
            position = data[data['YearMonth'] == point].index[0]
            ax.axvline(position, color = Colors[i], linestyle="--")

        markerLegend.append(mlines.Line2D([], [], color = Colors[i], marker = 'None', 
                        linestyle = '--', markersize=10, label = MarkerNames[i]))

    plt.legend(handles = markerLegend)

    # Save to file
    ax.get_figure().savefig(f'{OutputPrefix}_posts_by_months_area.png')


def mobile_showcase(data_repository):
    # Import sets as Pandas DataFrames
    Apple_PostsDF = pd.DataFrame([vars(post) for post in data_repository.data_sets[2].posts])
    Apple_VotesDF = pd.DataFrame([vars(vote) for vote in data_repository.data_sets[2].votes])

    Android_PostsDF = pd.DataFrame([vars(post) for post in data_repository.data_sets[3].posts])
    Android_VotesDF = pd.DataFrame([vars(vote) for vote in data_repository.data_sets[3].votes])

    Windows_PostsDF = pd.DataFrame([vars(post) for post in data_repository.data_sets[4].posts])
    Windows_VotesDF = pd.DataFrame([vars(vote) for vote in data_repository.data_sets[4].votes])


    # Number of new posts for each month and year
    Apple_PostsByMonths = posts_by_months(Apple_PostsDF)
    Android_PostsByMonths = posts_by_months(Android_PostsDF)
    Windows_PostsByMonths = posts_by_months(Windows_PostsDF)

    # Draw plots
    draw_plot_post_by_months(Apple_PostsByMonths, "Apple", "Apple", "Premiera nowej wersja systemu iOS", AppleReleaseDates, "purple")
    draw_plot_post_by_months(Android_PostsByMonths, "Android", "Android", "Premiera nowej wersja systemu Android", AndroidReleaseDates, "green")
    draw_plot_post_by_months(Windows_PostsByMonths, "Windows", "Windows Phone", "Premiera nowej wersja systemu Windows Phone", WindowsReleaseDates, "blue")

    # Draw common plot
    draw_plot_area([Apple_PostsByMonths, Android_PostsByMonths, Windows_PostsByMonths], [AppleReleaseDates, AndroidReleaseDates, WindowsReleaseDates], ["purple", "green", "blue"], ["Apple", "Android", "Windows Phone"], ["Premiera nowej wersja systemu iOS", "Premiera nowej wersja systemu Android", "Premiera nowej wersja systemu Windows Phone"], "Common")

    # Draw cross-platform plots
    draw_plot_post_by_months(Apple_PostsByMonths, "Apple", "Apple_AndroidRelease_",  "Premiera nowej wersja systemu Android", AndroidReleaseDates, "purple")
    #draw_plot_post_by_months(Android_PostsByMonths, "Android", "Android_AppleRelease_", "Premiera nowej wersja systemu iOS", AppleReleaseDates, "green")