import numpy as np
import pandas as pd
# Create a toy dataset with user-item ratings
df=pd.read_csv('dum_user_ratings.csv')
users = ["Divya", "Shashank", "Yashwal", "Gourav", "Prajwal", "Stuthi", "Simran", "Kuntal", "Soumya", "Anchal"]

ratings=[]
for i in df.index:
    ratings.append(list(df.loc[i, :]))

ratings = np.array(ratings)

# Calculate the mean rating for each user
user_means = np.mean(ratings, axis=1)

# Subtract the mean rating from each rating to get the deviations
deviations = ratings - user_means[:, np.newaxis]
# print(len(deviations))

# Calculate the item-item similarity matrix using cosine similarity
similarity = np.dot(deviations.T, deviations) / (np.linalg.norm(deviations.T, axis=1)[:, np.newaxis] * np.linalg.norm(deviations, axis=0))

# Get the top-k similar items for each item
k = 2
top_k = np.argsort(-similarity, axis=1)[:, 1:k+1]

# Predict the ratings for each user and item
predictions = np.zeros_like(ratings)

for user in range(ratings.shape[0]):
    for item in range(ratings.shape[1]):
        # Get the indices of the k most similar items
        similar_items = top_k[item]
        # Get the ratings for the k most similar items
        similar_ratings = ratings[user, similar_items]
        # Get the similarity values for the k most similar items
        similarities = similarity[item, similar_items]
        # Calculate the predicted rating as the weighted average of the similar ratings
        predictions[user, item] = np.sum(similar_ratings * similarities) / np.sum(similarities)

print(max(predictions[9]))

df=pd.DataFrame(predictions, columns=df.columns, index=users)
print(df)
hardcode_prod='07199265'
sim_users_rating=df.nlargest(4, hardcode_prod)
# print(len(sim_users_rating.max()))
for index, row in sim_users_rating.iterrows():
      print(row.idxmax())

df.to_csv('temp_result.csv')
