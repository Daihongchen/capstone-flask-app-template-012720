import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json
from tensorflow import keras
import pandas as pd 
import numpy as np

pd.set_option('display.float_format', '{:.1f}'.format)

def recommender(test_value):

    # Reload the model from the 2 files we saved
    # with open('src/models/model_config.json') as json_file:
    #     json_config = json_file.read()
    # model_mr = tf.keras.models.model_from_json(json_config) 
    # # # Load weights
    # model_mr.load_weights('src/models/weights_only.h5') 
    # load the model
    model_mr = tf.keras.models.load_model('src/models/mr_model.h5')
    
    ## pull the data for deploy
    data_mr = pd.read_csv('src/models/data_2018_mr.csv')

    movie_data = np.array(list(set(data_mr.movie)))
    user = np.array([test_value for i in range(len(movie_data))])
    
    predictions = model_mr.predict([user, movie_data])
    predictions = np.array([a[0] for a in predictions])
    recommended_movie_ids = (-predictions).argsort()[:5]

    recommend = data_mr[data_mr['movie'].isin(recommended_movie_ids)]
    recommend = recommend[[
                            'title', 
                            'average_rating',
                            'category', 
                            'description', 
                            'price', 
                            'links']].drop_duplicates()
    recommend = recommend.rename(columns={'title':'Title',
                                          'average_rating':'Overall_Rating',
                                          'category': 'Category',
                                          'description':'Description',
                                          'price': 'Price',
                                          'links': 'Links'})
    
    return recommend 


