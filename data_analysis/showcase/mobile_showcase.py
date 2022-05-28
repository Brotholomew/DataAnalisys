import pandas as pd

def most_popular_posts(PostsDT, VotesDT):
    # Select upvotes
    VotesDT = VotesDT[VotesDT['voteTypeId'] == 2]

    # Join posts with votes
    posts = pd.merge(PostsDT, VotesDT, how = 'inner', left_on = 'id', right_on = 'postId')

    # Count upvotes for each posts
    postUpVotes = posts.groupby(['id_x', 'title'])['id_x'].count().reset_index(name = 'UpVoteCount')

    # Sort by number of upvotes
    postUpVotes = postUpVotes.sort_values('UpVoteCount', ascending = False)

    # Get top 3 posts
    result = postUpVotes[['title', 'UpVoteCount']].head(3)
    print(result)


def mobile_showcase(data_repository):
    # Import sets as Pandas DataFrames
    Apple_PostsDT = pd.DataFrame([vars(post) for post in data_repository.data_sets[2].posts])
    Apple_VotesDT = pd.DataFrame([vars(vote) for vote in data_repository.data_sets[2].votes])

    Android_PostsDT = pd.DataFrame([vars(post) for post in data_repository.data_sets[3].posts])
    Android_VotesDT = pd.DataFrame([vars(vote) for vote in data_repository.data_sets[3].votes])

    Windows_PostsDT = pd.DataFrame([vars(post) for post in data_repository.data_sets[4].posts])
    Windows_VotesDT = pd.DataFrame([vars(vote) for vote in data_repository.data_sets[4].votes])

    # Print simple example - top 3 most liked posts
    print("Apple")
    print(most_popular_posts(Apple_PostsDT, Apple_VotesDT))

    print("Android")
    print(most_popular_posts(Android_PostsDT, Android_VotesDT))

    print("Windows")
    print(most_popular_posts(Windows_PostsDT, Windows_VotesDT))