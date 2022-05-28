import pandas as pd
import matplotlib.pyplot as plt

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

def posts_by_months(PostsDF, OutputPrefix, PointsOfInterest, Color):
    # Create column with year and month
    PostsDF['YearMonth'] = PostsDF['creationDate'].apply(lambda date: get_year_month(date))
    
    # Count created posts for each year and month
    postsByMonths = PostsDF.groupby('YearMonth')['id'].count().reset_index(name = 'Count')

    # Generate line plot
    markers = []
    for point in PointsOfInterest:
        rowNo = postsByMonths[postsByMonths['YearMonth'] == point].index[0]
        markers.append(rowNo)

    plt.figure()
    plt.plot(postsByMonths['YearMonth'], postsByMonths['Count'], '-D', markevery = markers, color = Color)
    plt.legend()
    plt.savefig(f"{OutputPrefix}_post_by_months.png")

    return postsByMonths


def mobile_showcase(data_repository):
    # Import sets as Pandas DataFrames
    Apple_PostsDF = pd.DataFrame([vars(post) for post in data_repository.data_sets[2].posts])
    Apple_VotesDF = pd.DataFrame([vars(vote) for vote in data_repository.data_sets[2].votes])

    Android_PostsDF = pd.DataFrame([vars(post) for post in data_repository.data_sets[3].posts])
    Android_VotesDF = pd.DataFrame([vars(vote) for vote in data_repository.data_sets[3].votes])

    Windows_PostsDF = pd.DataFrame([vars(post) for post in data_repository.data_sets[4].posts])
    Windows_VotesDF = pd.DataFrame([vars(vote) for vote in data_repository.data_sets[4].votes])


    # Number of new posts for each month and year
    Apple_PostsByMonths = posts_by_months(Apple_PostsDF, "Apple", AppleReleaseDates, "purple")
    Android_PostsByMonths = posts_by_months(Android_PostsDF, "Android", AndroidReleaseDates, "green")
    Windows_PostsByMonths = posts_by_months(Windows_PostsDF, "Windows", WindowsReleaseDates, "blue")

    test = pd.merge(Apple_PostsByMonths, Android_PostsByMonths, on = 'YearMonth', how = 'outer').fillna(0)
    test = pd.merge(test, Windows_PostsByMonths, on = 'YearMonth', how = 'outer').fillna(0)
    #test = Android_PostsByMonths[Android_PostsByMonths['YearMonth'].isin(Apple_PostsByMonths['YearMonth'])]

    ax = test.plot.area()


    for point in AppleReleaseDates:
        rowNo = test[test['YearMonth'] == point].index[0]
        ax.axvline(rowNo, color="red", linestyle="--")

    for point in AndroidReleaseDates:
        rowNo = test[test['YearMonth'] == point].index[0]
        ax.axvline(rowNo, color="yellow", linestyle="--")

    for point in WindowsReleaseDates:
        rowNo = test[test['YearMonth'] == point].index[0]
        ax.axvline(rowNo, color="blue", linestyle="--")

    ax.get_figure().savefig('test.png')

    posts_by_months(Apple_PostsDF, "AppleWithAndroidRelease", AndroidReleaseDates, "green")

    print(test)