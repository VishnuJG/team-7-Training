from surprise import Dataset
from surprise import Reader
from surprise import SVD
from surprise import accuracy
from surprise.model_selection import train_test_split
from dummy_data_creation import mapping_dict
import pandas as pd
import pickle

def map_to_productID(my_dict, value):
  print("mapping", my_dict)
  return list(filter(lambda x: my_dict[x] == value, my_dict))[0]


def get_Iu(uid, trainset):
    """ return the number of items rated by given user
    args: 
      uid: the id of the user
    returns: 
      the number of items rated by the user
    """
    try:
        return len(trainset.ur[trainset.to_inner_uid(uid)])
    except ValueError: # user was not part of the trainset
        return 0
    

def get_Ui(iid, trainset):
    """ return number of users that have rated given item
    args:
      iid: the raw id of the item
    returns:
      the number of users that have rated the item.
    """
    try: 
        return len(trainset.ir[trainset.to_inner_iid(iid)])
    except ValueError:
        return 0

def collab_recommender():
    # Load data from a file with the following format: user_id, item_id, rating
    file_path = 'user_ratings.csv'
    reader = Reader(line_format='user item rating', sep=',', skip_lines=1)
    data = Dataset.load_from_file(file_path, reader=reader)

    # Split data into train and test sets
    trainset, testset = train_test_split(data, test_size=0.2)

    # Train an ALS model on the train set
    model = SVD(n_factors=50, n_epochs=20, lr_all=0.005, reg_all=0.02)
    model.fit(trainset)

    # Save and load the trained model
    pickle.dump(model, open('model.pkl', 'wb'))
    pickled_model = pickle.load(open('model.pkl', 'rb'))

    # Predict ratings on the test set
    predictions = pickled_model.test(testset)
    # print(predictions)

    # Compute RMSE on the test set
    rmse = accuracy.rmse(predictions)

    df = pd.DataFrame(predictions, columns=['uid', 'iid', 'rui', 'est', 'details'])
    df['Iu'] = df.apply(lambda x: get_Iu(x['uid'], trainset=trainset), axis=1)
    # df['Iu'] = df.uid.apply(get_Iu, args=(trainset))
    df['Ui'] = df.apply(lambda x: get_Ui(x['iid'], trainset=trainset), axis=1)
    # df['Ui'] = df.iid.apply(get_Ui, args=trainset)
    df['err'] = abs(df.est - df.rui)

    # Get top 10 recommendations
    best_predictions = df.sort_values(by='err')[:10]
    worst_predictions = df.sort_values(by='err')[-10:]
    top_n = best_predictions['iid'].tolist()[:10]
    print("top_n", top_n)
    top_recs = [map_to_productID(mapping_dict, str(x)) for x in top_n if x in mapping_dict.values()]
    print("top_recs", top_recs)
    return top_recs

# print(best_predictions)

# Recommend items to a user
# user_id = '7'
# num_items = 4
# user_items = [i[0] for i in trainset.ur[int(user_id)]]
# all_items = list(model.trainset.ir.keys())
# unseen_items = set(all_items) - set(user_items)
# # print(unseen_items)
# # print(data.all_items())
# testset = [[user_id, item_id, 4.] for item_id in unseen_items]
# predictions = model.test(testset)
# # print(sorted(predictions, key=lambda x: x.est, reverse=True))
# top_n = sorted(predictions, key=lambda x: x.est, reverse=True)[:num_items]
# # for pred in top_n:
# #     print(map_to_productID(mapping_dict, pred.iid))
# print([pred.iid for pred in top_n])
# print([map_to_productID(mapping_dict, pred.iid) for pred in top_n])

def addd(num, num2):
    return (num + num2)

data = [['tom', 10], ['nick', 15], ['juli', 14]]
df = pd.DataFrame(data, columns=['Name', 'Age'])
df['new'] = df.Age.apply