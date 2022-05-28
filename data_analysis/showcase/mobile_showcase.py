import pandas as pd

def mobile_showcase(data_repository):
    test = pd.DataFrame([vars(s) for s in data_repository.data_sets[0].posts])
    print(test)