import os
import pandas as pd
import numpy as np
#Problem
from utile import target, keeping_col


#Fonction pour randomiser les joueurs
def randomize_player(df):
    
    '''
    Bla bla bla, information de la fonction
    '''

    #Player's informations
    winner_col = ['winner','b365w','wrank']
    loser_col = ['loser','b365l','lrank']
    #Generate random 0,1
    data = list(np.random.choice([0, 1], len(df)))

    #Join player informations in list
    df1 = df.assign(winner_info = df[winner_col].values.tolist()
                    ,loser_info =  df[loser_col].values.tolist()
                    ,random = data
                     )
    #Randomize player information P1 or P2
    df2 = df1\
         .assign(p1 = np.where(df1['random'] == 0, df1['winner_info'], df1['loser_info'])
                ,p2 =np.where(df1['random'] == 1, df1['winner_info'], df1['loser_info']) 
                )\
                    .loc[:,['p1','p2']]
    
    #Create tidy data set without list
    df_random_player = df2\
        .join(df2['p1']\
              .apply(pd.Series))\
                .rename(columns={0: 'p1_Name'
                                 , 1: 'p1_b365'
                                 , 2: 'p1_rank'}
                                 )\
                                    .join(df2['p2']\
                                          .apply(pd.Series))\
                                            .rename(columns={0: 'p2_Name'
                                                             , 1: 'p2_b365'
                                                             , 2: 'p2_rank'}
                                                            )\
                                                                .drop(['p1','p2'],axis=1)

    return(df_random_player)#Return a dataset after randomize player's informations


#Fonction pour créer le data set prêt pour le feature eng
def create_df_feature_eng(df_base, df_add):
    #Data set with player's information and match's information
    df_player_and_match = df_base[keeping_col+[target]].join(df_add)
    return(df_player_and_match)


#Main function
def preprocess_data(df):
    '''
    bla bla bla
    '''
    data = df\
        .rename(columns={'Best of': 'best_of'})\
            .assign(Date=lambda x: pd.to_datetime(x.Date, format='%Y-%m-%d'))\
                .rename(columns=str.lower)\
                    .query("comment=='Completed'")\
                        .dropna()\
                            .copy()
    
    #Randomize player's data

    df_random_player = randomize_player(data)
    df_player_and_match = create_df_feature_eng(data, df_random_player)

    return(df_player_and_match)

