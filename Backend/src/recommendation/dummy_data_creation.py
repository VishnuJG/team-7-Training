import random
import pandas as pd
import csv
import numpy as np
import itertools

df=pd.read_json('../../../data/out.json')

products = df['uniqueId']
users = [i for i in range(1, 11)]

# Map product IDs to an integral ID using dictionary 
product_user_list = list(itertools.chain(users, products))
# print(product_user_list)
mapping_dict = {}
num = 0
for item in product_user_list:
    num = num + 1
    mapping_dict[item] = num

user_ids = [num for num in range(1, 11)]
product_ids = [num for num in range(11, 3010)]
# print(mapping_dict)


# create random ratings 
ratings = {}
final_df=pd.DataFrame(columns=['user_id', 'product_id', 'rating'])
print(users)
for user in users:
    
    for prod in products:
        temp_df=pd.DataFrame([[user, mapping_dict[prod], round(random.randint(0, 5), 1)]],columns=['user_id', 'product_id', 'rating'])
        final_df=pd.concat([final_df, temp_df])
final_df.reset_index(drop=True, inplace=True)
# print(final_df)
final_df.to_csv('user_ratings.csv', index=False)


