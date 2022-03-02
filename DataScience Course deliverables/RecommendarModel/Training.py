import pandas as pd
from surprise import SVD
from surprise import Dataset
from surprise import accuracy
from surprise import Reader
from surprise.model_selection import train_test_split
from collections import defaultdict
import json


def pull_data(file_name):
    all_records = pd.read_csv(file_name)
    return all_records


def top_records(all_records):
    reviewerID = all_records.groupby('reviewerID').count()
    top_user = reviewerID[reviewerID['overall'] >= 50].index
    topuser_ratings_df = all_records[all_records['reviewerID'].isin(top_user)]

    asin = all_records.groupby('asin').count()
    top_prod = asin[asin['overall'] >= 50].index
    top_records = topuser_ratings_df[topuser_ratings_df['asin'].isin(top_prod)]
    return top_records


def prepare_for_training(top_records):
    reader = Reader(rating_scale=(1.0, 5.0))
    data = Dataset.load_from_df(top_records[['reviewerID', 'asin', 'overall']], reader)
    trainset, testset = train_test_split(data, test_size=.3, random_state=0)

    return trainset, testset


def train_model(training_data):
    svd_model = SVD(n_factors=50, reg_all=0.02)
    svd_model.fit(training_data)
    return svd_model


def test_model(testing_data, model):
    test_pred = model.test(testing_data)
    print(accuracy.rmse(test_pred))
    return test_pred


def get_top_n(predictions, n=3):
    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


all_records = pull_data('electronics.csv')

top_records = top_records(all_records)

trainset, testset = prepare_for_training(top_records)

train_model = train_model(trainset)

test_model = test_model(testset, train_model)

top_n = get_top_n(test_model, n=3)

# Print the recommended items for each user
with open("predictions.json", "w") as f:
    for uid, user_ratings in top_n.items():
        print(uid, [iid for (iid, _) in user_ratings])
        record = {uid: [iid for (iid, _) in user_ratings]}
        f.write(json.dumps(record))
        f.write("\n")





