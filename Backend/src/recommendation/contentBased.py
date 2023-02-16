import sys
sys.path.append('..')
import operations, models
from operations.database import Database

# from queries import *
import json
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import psycopg2


class ContentBasedRecommender:

    def recommender(self, uniqueID):
        db=Database()
        x = db.read_from_db("SELECT uniqueID, description, title from product_table;")
        df = pd.DataFrame(x, columns=['uniqueID','Description', 'Title'])
        df_feature_matrix = df['Title'].str.lower() + ' ' + df['Description'].str.lower()

        # print(df_feature_matrix[0])
        # print(df)

        vectorizer = CountVectorizer(stop_words='english')
        vectorized = vectorizer.fit_transform(df_feature_matrix)

        similarities = cosine_similarity(vectorized)
        # df_processed = pd.DataFrame(similarities).reset_index()
        df_processed = pd.DataFrame(similarities, columns=df['Title']+' '+ df['Description'], index=df['Title']+' '+ df['Description']).reset_index()
        # df_processed = pd.DataFrame(similarities, columns=['Description']).reset_index()
        # print(df_processed.columns)
        # print(similarities)
        desc_dyn=df[df['uniqueID'] == str(uniqueID)]['Description']
        title_dyn=df[df['uniqueID'] == str(uniqueID)]['Title']
        

        input_prod= str(title_dyn.iloc[-1]) +' '+  desc_dyn.iloc[-1] 
        # print(input_prod)
        # print(df_processed.nlargest(5,input_prod).iloc[1:1,:])
        sim_score = pd.DataFrame(df_processed.nlargest(5,input_prod)[input_prod])
        recommendations = pd.DataFrame(df_processed.nlargest(5,input_prod)['index'])
        recommendations = recommendations[recommendations['index']!=input_prod]
        sim_score.columns=['Score']
        # print(recommendations)

        temp = pd.concat([df.iloc[recommendations.index], sim_score], axis=1)        
        y = db.read_from_db("SELECT uniqueId, price, title, image_url from product_table where uniqueId in %s", (tuple(temp['uniqueID'].dropna()), ))        
        return y