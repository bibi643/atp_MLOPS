
from fastapi import FastAPI, Query
from typing import Optional
import pandas as pd
import joblib
from datetime import datetime
from typing import Optional
from data_loader import load_data










df_jb= pd.read_csv('df_ATP_clean.csv')
df_jb=df_jb.drop(labels='Unnamed: 0',axis=1)

#target= df['WP1']
data=df_jb.drop(labels='WP1',axis=1)
data_raw=data.round(1)
 
#Game data_base
game_db=data_raw.to_dict('records')


data=data_raw[['Round','Series','Court','Surface','Player1_rank','Player1_ELO','Player2_rank','Player2_ELO']]
data=pd.get_dummies(data,columns=['Round','Series','Court','Surface'],prefix='',prefix_sep='')
data=data.rename(columns={'1st Round':'1st_Round',
                                      '2nd Round': '2nd_Round',
                                      '3rd Round':'3rd_Round',
                                      '4th Round':'4th_Round',
                                      'Round Robin':'Round_Robin',
                                      'The Final':'Final',
                                      'Grand Slam':'Grand_Slam',
                                      'International Gold':'International_Gold',
                                      'Masters 1000':'Master_1000',
                                      'Masters Cup':'Master_Cup'})



#player database
player1_base=df_jb[['Player1_name','Player1_rank','Player1_ELO']]
player2_base=df_jb[['Player2_name','Player2_rank','Player2_ELO']]
player1_base=player1_base.rename(columns={'Player1_name': 'Player_name',
                                  'Player1_rank':'Player_rank',
                                  'Player1_ELO':'Player_ELO'})
player2_base=player2_base.rename(columns={'Player2_name': 'Player_name',
                                  'Player2_rank':'Player_rank',
                                  'Player2_ELO':'Player_ELO'})
player_base=pd.concat([player1_base,player2_base],axis=0)
player_base.head()
#data base player
player_base['Player_name']=player_base['Player_name'].str.upper()

#Ici on va prendre la derniere actualisation du joueur. Cela devrait servir pour la prediction de futur match, lorsque le user choisira les deux jouerus pour une prediction future.
player_base_updated=player_base.groupby(by='Player_name').last()
#player_base_updated.reset_index
player_base_updated=player_base_updated.sort_values(by=['Player_name']).reset_index()
player_base_updated= player_base_updated.to_dict('records')



#Tournoi data base
tournois_db=df_jb[['ATP','Location','Date','Tournament','Series','Court','Surface']]
tournois_db=tournois_db.groupby(by=['Tournament']).first()
tournois_db=tournois_db.reset_index()
tournois_db=tournois_db.set_index('Tournament')
#ici les characteristiques du tournoi sont dummifiees. Sans doute utile lorsque le user choisira deux joueru maia aussi le nom du tournoi.
tournois_db=pd.get_dummies(tournois_db,columns=['Series','Court','Surface'],prefix='',prefix_sep='')
tournois_db=tournois_db.drop(labels='ATP',axis=1)
tournois_db=tournois_db.sort_values(by=['Tournament'])
tournois_db=tournois_db.reset_index()
tournois_db=tournois_db.to_dict('records')





from data_loader import load_data
from utile import path_db
from preprocessing import preprocess_data
from feature_eng import feature_eng
from modele import logistic_regression_model
from modele_training import train_logistic_regression_model
from modele_predict import accuracy_and_confusion_matrix
from model_save import save_model_pickle, save_model_joblib

# 01 Import data
print('Lancement du code 01: data_loader.py')
df = load_data(path_db)
print('taille du dataframe:', df.shape)

# 02 Preprocessing data
print('lancement du code 2: preprocessing.py')
test = preprocess_data(df)
print('output preprocess:', test.shape)
print('colonne names:', test.columns)

# 03 feature enginering
print('Lancement du code 3: feature_eng.py')
X_train, X_test, y_train, y_test = feature_eng(test)

reg=joblib.load('atp_logistic_model.joblib')


api=FastAPI(
    title='Paris sportifs',
    description='API propre faite sur FastAPI')




@api.get('/home')
def get_home():
    """Return greetings
    """
    return {'Greetings':'Bienvenue'}


@api.get('/player_from_list')
def get_player_from_list(joueur1_choisi: str = Query("Joueur ATP", enum={joueur['Player_name']for joueur in player_base_updated}),joueur2_choisi: str = Query("Joueur ATP", enum={joueur['Player_name']for joueur in player_base_updated})):
    p1=list(filter(lambda x:x.get('Player_name')==joueur1_choisi,player_base_updated))
    p2=list(filter(lambda x:x.get('Player_name')==joueur2_choisi,player_base_updated))
    return p1,p2
    




@api.get('/tournament_from_list')
def get_tournament_from_list(tournois_choisi: str = Query("TOURNAMENT_LIST_ATP", enum={tournament['Tournament']for tournament in tournois_db})):
   # return {'selected': tournois_choisi}
    t=list(filter(lambda y:y.get('Tournament')==tournois_choisi,tournois_db))
    return t


@api.get('/new_game')# does not work yet
def new_game(date:str, player1: str, player2:str ):
    """Return the game between 2 players on a specific date"""
    #player1=player1.upper()
    #player2=player2.upper()
    try:
        specific_game=data_raw[((data_raw['Player1_name']==player1) | (data_raw['Player2_name']==player1))&((data_raw['Player1_name']==player2) | (data_raw['Player2_name']==player2))&(data_raw['Date']==date)]
        specific_game=specific_game.to_dict('records')
        return specific_game


    except IndexError:
        {}
    


@api.get('/new_game_2')
#@get_player_from_list# does not work yet
def new_game_list(date:str, player1: str=Query("Joueur ATP", enum={joueur['Player_name']for joueur in player_base_updated}), player2:str=Query("Joueur ATP", enum={joueur['Player_name']for joueur in player_base_updated})):
    """Return the game between 2 players on a specific date"""
    #player1=player1.upper()
    #player2=player2.upper()
    try:
        specific_game= game_db[((game_db['Player1_name']==player1) | (game_db['Player2_name']==player1))&((game_db['Player1_name']==player2) | (game_db['Player2_name']==player2))&(game_db['Date']==date)]
        #specific_game=specific_game
        #specific_game=data_raw[((data_raw['Player1_name']==(player1[0]['Player_name'])) | (data_raw['Player2_name']==(player1[0]['Player_name'])))&((data_raw['Player1_name']==(player2[0]['Player_name'])) | (data_raw['Player2_name']==(player2[0]['Player_name'])))&(data_raw['Date']==date)]
        #specific_game=specific_game.to_dict('records')
        return specific_game


    except IndexError:
        {}
    

@api.get('/one_player')
def get_player(player1: str=Query("Joueur ATP", enum={joueur['Player_name']for joueur in player_base_updated})):#, player2:str=Query("Joueur ATP", enum={joueur['Player_name']for joueur in player_base_updated})))
        #p1=list(filter(lambda x:x.get('Player_name')==player1,player_base_updated))
        return player1


@api.get('/players_game')
def players_match(player1: str, player2: str):
    """Retruns the name, rank, ELO number of players of a selected game"""
    player1=player1.upper()
    player2=player2.upper()
    try:
        p1=list(filter(lambda x:x.get('Player_name')==player1,player_base_updated))
        p2=list(filter(lambda x:x.get('Player_name')==player2,player_base_updated))
        return p1,p2
    except IndexError:
        {}
    
   
    
   


@api.get('/tournois')
def get_tournois(tournois:str,location:Optional[str]=None,date:Optional[str]=None):
    """Return the tournament name and series and characteristics based on location or date if specified"""
    try:       
        t=list(filter(lambda y:y.get('Tournament')==tournois,tournois_db))
        return t
    except IndexError:
        {}
    
   




@api.get('/predictions')
def new_predictions(player1:str,player2:str,date:str,tournois:Optional[str]=None,):
    """Returns the winner of a specific game."""
    predictions_ds= reg.predict(player1,player2,date,tournois)
    return{'predictions': predictions_ds}
