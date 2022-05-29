from showcase.cluster2_showcase import cluster2_score_length, cluster2_test, cluster2_showcase
from dbo.data_repository import DataRepository
from showcase.rocket_showcase import ridge_regression_fit_score_post_length, rocket_score_viewcount, \
    ridge_regression_fit_score_viewcount
from utils.utils import Mailbox


if __name__ == "__main__":
    Mailbox.debugLevel = 1

    cluster2_showcase()
