import sys
sys.path.append('..')
import Operations
from Operations.database import Database

# from queries import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
# from collaborative_filtering import top_n


class ContentBasedRecommender:

    def recommender(self, uniqueID):
        db=Database()
        x = db.read_from_db("SELECT uniqueID, description, title from product_table;")
        df = pd.DataFrame(x, columns=['uniqueID','Description', 'Title'])
        try:
            df_processed=pd.read_pickle('processedDF.pkl')
        except:
            df_feature_matrix = df['Title'].str.lower() + ' ' + df['Description'].str.lower()
            vectorizer = CountVectorizer(stop_words='english')
            vectorized = vectorizer.fit_transform(df_feature_matrix)
            similarities = cosine_similarity(vectorized)
            df_processed = pd.DataFrame(similarities, columns=df['Title']+' '+ df['Description'], index=df['Title']+' '+ df['Description']).reset_index()
            df_processed.to_pickle('processedDF.pkl')
        
        desc_dyn=df[df['uniqueID'] == str(uniqueID)]['Description']
        title_dyn=df[df['uniqueID'] == str(uniqueID)]['Title']
        input_prod= str(title_dyn.iloc[-1]) +' '+  desc_dyn.iloc[-1] 

        sim_score = pd.DataFrame(df_processed.nlargest(5,input_prod)[input_prod])
        recommendations = pd.DataFrame(df_processed.nlargest(5,input_prod)['index'])
        recommendations = recommendations[recommendations['index']!=input_prod]
        sim_score.columns=['Score']

        temp = pd.concat([df.iloc[recommendations.index], sim_score], axis=1)        
        y = db.read_from_db("SELECT uniqueId, price, title, image_url from product_table where uniqueId in %s", (tuple(temp['uniqueID'].dropna()), ))        
        return y


    def weighted_preds(self, content_preds):
        df_weighted = content_preds['Score']
        

