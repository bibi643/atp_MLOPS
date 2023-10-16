#Hard values

import os
import pandas as pd
import numpy as np

keeping_col =[#'atp'
              'location'
              ,'tournament'
              ,'date'
              ,'series'
              ,'surface'
              ,'round'
              ,'best_of'
              ,'proba_elo'
              ]

target='winner'

path_root = "https://github.com/bibi643/atp_MLOPS/raw/main"
path_db = os.path.join(path_root, "atp_data.csv")

def load_data(path :str):

    df = pd.read_csv(path, sep=',')
    
    return(df)


def frequency_encoding(df, column_name):
    # Créer un dictionnaire de fréquence pour la colonne spécifiée
    freq_encoding = df[column_name].value_counts(normalize=True).to_dict()
    
    # Appliquer l'encodage de fréquence à la colonne
    df[column_name + '_encoded'] = df[column_name].map(freq_encoding)
    
    return df


def randomize_player(df):
    
    '''
    Bla bla bla, information de la fonction
    '''

    #Player's informations
    winner_col = ['winner','b365w','elo_winner','wrank']
    loser_col = ['loser','b365l','elo_loser','lrank']
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
                                 , 2: 'p1_elo'
                                 , 3: 'p1_rank'}
                                 )\
                                    .join(df2['p2']\
                                          .apply(pd.Series))\
                                            .rename(columns={0: 'p2_Name'
                                                             , 1: 'p2_b365'
                                                             , 2: 'p2_elo'
                                                             , 3: 'p2_rank'}
                                                            )\
                                                                .drop(['p1','p2'],axis=1)

    return(df_random_player)#Return a dataset after randomize player's informations


def create_df_feature_eng(df_base, df_add):
    #Data set with player's information and match's information
    df_player_and_match = df_base[keeping_col+[target]].join(df_add)
    return(df_player_and_match)
