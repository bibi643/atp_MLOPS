
import pandas as pd
from data_loader import load_data
from utile import path_db
from preprocessing import preprocess_data
from feature_eng import feature_eng
from modele import logistic_regression_model
from modele_training import train_logistic_regression_model
from modele_predict import accuracy_and_confusion_matrix
from model_save import save_model_pickle, save_model_joblib
from fastapi import FastAPI, Query
from typing import Optional
import pandas as pd
import joblib
from datetime import datetime
from typing import Optional
from data_loader import load_data
from feature_eng import feature_eng_predict
from model_save import load_model


df=load_data('atp_data.csv')
df_preprocessed=preprocess_data(df)

#Player db
player1_base=df_preprocessed[['p1_Name','p1_rank','p1_elo']]
player2_base=df_preprocessed[['p2_Name','p2_rank','p2_elo']]
player1_base=player1_base.rename(columns={'p1_Name': 'Player_name',
                                  'p1_rank':'Player_rank',
                                  'p1_elo':'Player_ELO'})
player2_base=player2_base.rename(columns={'p2_Name': 'Player_name',
                                  'p2_rank':'Player_rank',
                                  'p2_elo':'Player_ELO'})
player_base=pd.concat([player1_base,player2_base],axis=0)
player_base=player_base.reset_index().drop(columns='index')
player_base_updated=player_base.groupby(by='Player_name').last()
player_base_updated=player_base_updated.sort_values(by=['Player_name']).reset_index()
player_base_updated= player_base_updated.to_dict('records')


#Tournament DB

tournois_db=df_preprocessed[['location','date','tournament','series','surface']]
tournois_db=tournois_db.groupby(by=['tournament']).first()
tournois_db=tournois_db.reset_index()
tournois_db=tournois_db.set_index('tournament')
#ici les characteristiques du tournoi sont dummifiees. Sans doute utile lorsque le user choisira deux joueru maia aussi le nom du tournoi.
tournois_db=pd.get_dummies(tournois_db,columns=['series','surface'],prefix='',prefix_sep='')

tournois_db=tournois_db.sort_values(by=['tournament'])
tournois_db=tournois_db.reset_index()
tournois_db=tournois_db.to_dict('records')


#API
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
    """Return the datas of the selected players"""
    p1=list(filter(lambda x:x.get('Player_name')==joueur1_choisi,player_base_updated))
    p2=list(filter(lambda x:x.get('Player_name')==joueur2_choisi,player_base_updated))
    return p1,p2





@api.get('/tournament_from_list')
def get_tournament_from_list(tournois_choisi: str = Query("TOURNAMENT_LIST_ATP", enum={tournament['tournament']for tournament in tournois_db})):
    """Return the datas of the selected tournament"""
    t=list(filter(lambda y:y.get('tournament')==tournois_choisi,tournois_db))
    return t



@api.get('/new_game')
def new_game_list(date:str, player1: str=Query("Joueur ATP", enum={joueur['Player_name']for joueur in player_base_updated}), player2:str=Query("Joueur ATP", enum={joueur['Player_name']for joueur in player_base_updated})):
    """Return the game between 2 players on a specific date"""
    #player1=player1.upper()
    #player2=player2.upper()
    try:
         specific_game=df_preprocessed[((df_preprocessed['p1_Name']==player1) | (df_preprocessed['p2_Name']==player1))&((df_preprocessed['p1_Name']==player2) | (df_preprocessed['p2_Name']==player2))&(df_preprocessed['date']==date)]
         specific_game=specific_game.to_dict('records')
         return specific_game
        
    


    except IndexError:
        {}




@api.get('/new_prediction')
def new_game_pred(date:str, player1: str=Query("Joueur ATP", enum={joueur['Player_name']for joueur in player_base_updated}), player2:str=Query("Joueur ATP", enum={joueur['Player_name']for joueur in player_base_updated})):
    """Return the game between 2 players on a specific date"""
    #player1=player1.upper()
    #player2=player2.upper()
    specific_game=df_preprocessed[((df_preprocessed['p1_Name']==player1) | (df_preprocessed['p2_Name']==player1))&((df_preprocessed['p1_Name']==player2) | (df_preprocessed['p2_Name']==player2))&(df_preprocessed['date']==date)]
    specific_game=specific_game.to_dict('records')
    nd=pd.DataFrame.from_records(specific_game)
    x_new=feature_eng_predict(nd)
    model = load_model('./atp_logistic_model.pkl')
    if model.predict(x_new.head(5))==1 :

        winner = '1'
        nom = nd.p1_Name
        cote = nd.p1_b365

    else:
        
        winner = '2'
        nom = nd.p2_Name
        cote = nd.p2_b365

    return {'Winner': winner,
           'Nom': nom,
           'Cote': cote}


    

    
    

    
    

 
