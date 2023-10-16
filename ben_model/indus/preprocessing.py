import os
os.chdir("/home/ubuntu/bet_tennis/indus/")
import pandas as pd
import numpy as np

from utile import keeping_col, load_data, path_db , frequency_encoding, randomize_player,create_df_feature_eng



def preprocess_data(path_df):
    #Load data 
    df = load_data(path=path_df)\
        .rename(columns={'Best of': 'best_of'})\
            .assign(Date=lambda x: pd.to_datetime(x.Date, format='%Y-%m-%d'))\
                .rename(columns=str.lower)\
                    .query("comment=='Completed'")\
                        .dropna()\
                            .copy()
    
    #Randomize player's data

    df_random_player = randomize_player(df)
    df_player_and_match = create_df_feature_eng(df, df_random_player)
    return(df_player_and_match)
 

temp = preprocess_data(path_db)

print('Voici la taille du df: ', temp.shape)

print('Les colonnes du df:',  temp.columns)