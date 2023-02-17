import random
import pandas as pd
import csv
import numpy as np

df=pd.read_json('../../../data/out.json')
# print(df)

products = df['uniqueId']
users = ["Divya", "Shashank", "Yashwal", "Gourav", "Prajwal", "Stuthi", "Simran", "Kuntal", "Soumya", "Anchal"]
# users = [i for i in range(1, 11)]
ratings = {}

# Generate 100 ratings for each product
# for product in products:
#     for i in range(100):
#         rating = round(random.uniform(1, 5), 1)
#         ratings.append({"product": product, "rating": rating})
# for product in products:
#     product_ratings = []
#     for i in range(100):
#         rating = round(random.uniform(1, 5), 1)
#         product_ratings.append(rating)
#     ratings[product] = product_ratings
# # Print the generated ratings
# print(ratings)
# for rating in ratings:
#     print(f"{rating['product']}: {rating['rating']}")


ratings = np.zeros((len(users), len(products)))
for i, user in enumerate(users):
    for j, product in enumerate(products):
        rating = round(random.randint(0, 5), 1)
        ratings[i,j] = rating

# ratings = np.zeros((len(products), len(users)))
# for i, prod in enumerate(products):
#     for j, users in enumerate(users):
#         rating = round(random.randint(0, 5), 1)
#         ratings[i,j] = rating

print(ratings)
# # Print the table of ratings
# print("{:<10}".format(""), end="")
# for product in products:
#     print("{:<12}".format(product), end="")
# print("")
# for i, user in enumerate(users):
#     print("{:<10}".format(user), end="")
#     for j in range(len(products)):
#         print("{:<12}".format(ratings[i,j]), end="")
#     print("")


final_df=pd.DataFrame(ratings, columns=products)
# final_df=pd.DataFrame(columns=['user_id', 'item_id', 'rating'])
# print(users)
# for user in users:
    
#     for prod in products:
#         temp_df=pd.DataFrame([[user, prod, round(random.randint(0, 5), 1)]],columns=['user_id', 'item_id', 'rating'])
#         # final_df=final_df.append({'user_id':user, 'item_id':prod, 'rating':round(random.randint(0, 5), 1),}, ignore_index=True)
#         final_df=pd.concat([final_df, temp_df])
        

# final_df.reset_index(drop=True, inplace=True)
# df.set_index([users, 'userId'])


# final_df['userId']=users
# final_df.set_index(['userId'])
# final_df.reset_index()
print(final_df)
final_df.to_csv('dum_user_ratings.csv')

# Map product IDs to an integral ID
