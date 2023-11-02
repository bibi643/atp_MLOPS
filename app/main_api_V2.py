

#IMPORT THE PACKAGES
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

import joblib


from data_loader import load_data
from feature_eng import feature_eng_predict
from model_save import load_model
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, status, Body, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import time
from admin_func import get_current_admin
from user_func import UserSchema, check_user, token_response, sign_jwt, decode_jwt, JWTBearer


#LOAD THE DATA
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
player_base_updated_df=player_base_updated.sort_values(by=['Player_name']).reset_index().reset_index()
player_base_updated_df['index']=player_base_updated_df['index']+1
player_base_updated_df=player_base_updated_df.rename(columns={'index':'Player_ID'})
player_base_updated_db= player_base_updated_df.to_dict('records')


#Tournament DB

tournois_df=df_preprocessed[['location','date','tournament','series','surface']]
tournois_df=tournois_df.groupby(by=['tournament']).first()
tournois_df=tournois_df.reset_index().reset_index().rename(columns={'index':'Tournois_ID'})
tournois_df['Tournois_ID']=tournois_df['Tournois_ID']+1

#ici les characteristiques du tournoi sont dummifiees. Sans doute utile lorsque le user choisira deux joueru maia aussi le nom du tournoi.
tournois_df_dum=pd.get_dummies(tournois_df,columns=['series','surface'],prefix='',prefix_sep='')
tournois_db=tournois_df_dum.to_dict('records')




#CLASS TO UPDATE THE API WITH NEW DATAS (ROUTE PUT)
class Player(BaseModel):
    name: str
    rank: int
    elo: Optional[float] = 1500.0


class Tournament(BaseModel):
    name: str
    location: str
    date: datetime
    series: str
    surface: str



#CLASS FOR SECURITY
#class UserSchema(BaseModel):
  #  username: str
  #  password: str
  #  email: str





users= []



# Configuration pour le JWT
JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"








#API
api=FastAPI(
    title='Paris sportifs',
    description='API propre faite sur FastAPI',
    openapi_tags=[
        {'name':'home',
         'description':'Default fucntion'
        },
        {'name':'Players',
        'description':'Functions that are used to deal with players'},
        {'name':'Tournaments',
         'description':'Functions that are used to deal with tournaments.'},
         {'name':'Predictions',
          'description':'Functions that are used to deal with predictions.'}
          
    ])








@api.get('/home',tags=['home'],dependencies=[Depends(JWTBearer())])
def get_home():
    """Return greetings
    """
    return {'Greetings':'Bienvenue'}


@api.get('/player_from_list',tags=['Players'],dependencies=[Depends(JWTBearer())])
def get_player_from_list(joueur1_choisi: str = Query("Joueur ATP", enum={joueur['Player_name']for joueur in player_base_updated_db}),joueur2_choisi: str = Query("Joueur ATP", enum={joueur['Player_name']for joueur in player_base_updated_db})):
    """Return the datas of the selected players"""
    p1=list(filter(lambda x:x.get('Player_name')==joueur1_choisi,player_base_updated_db))
    p2=list(filter(lambda x:x.get('Player_name')==joueur2_choisi,player_base_updated_db))
    return p1,p2





@api.get('/tournament_from_list',tags=['Tournaments'],dependencies=[Depends(JWTBearer())])
def get_tournament_from_list(tournois_choisi: str = Query("TOURNAMENT_LIST_ATP", enum={tournament['tournament']for tournament in tournois_db})):
    """Return the datas of the selected tournament"""
    t=list(filter(lambda y:y.get('tournament')==tournois_choisi,tournois_db))
    return t



@api.get('/new_game',tags=['Players'],dependencies=[Depends(JWTBearer())])
def new_game_list(date:str=Query('YYYY-MM-DD'), player1: str=Query("Joueur ATP", enum={joueur['Player_name']for joueur in player_base_updated_db}), player2:str=Query("Joueur ATP", enum={joueur['Player_name']for joueur in player_base_updated_db})):
    """Return the game between 2 players on a specific date"""
    #player1=player1.upper()
    #player2=player2.upper()
    try:
         specific_game=df_preprocessed[((df_preprocessed['p1_Name']==player1) | (df_preprocessed['p2_Name']==player1))&((df_preprocessed['p1_Name']==player2) | (df_preprocessed['p2_Name']==player2))&(df_preprocessed['date']==date)]
         specific_game=specific_game.to_dict('records')
         return specific_game
        
    


    except IndexError:
        {}




@api.get('/new_prediction',tags=['Predictions'],dependencies=[Depends(JWTBearer())])
def new_game_pred(date:str=Query('YYYY-MM-DD'), player1: str=Query("Joueur ATP", enum={joueur['Player_name']for joueur in player_base_updated_db}), player2:str=Query("Joueur ATP", enum={joueur['Player_name']for joueur in player_base_updated_db})):
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


    

@api.put('/players',tags=['Players'])
def put_player(player: Player,username: str = Depends(get_current_admin)):
    """Add a new player in the player database"""
    new_id = max(player_base_updated_db, key=lambda u: u.get('Player_ID'))['Player_ID']
    new_player= {
        'Player_ID': new_id +1,
        'Player_name': player.name,
        'Player_rank': player.rank,
        'Player_ELO': player.elo
    }
    player_base_updated_db.append(new_player)
    return new_player #player base_updated not being updated

    

@api.put('/tournois',tags=['Tournaments'])
def put_tournoi(new_tournois: Tournament,username: str = Depends(get_current_admin)):
    new_id_tournois = max(tournois_db, key=lambda u: u.get('Tournois_ID'))['Tournois_ID']
    new_tournois= {
        'Tournois_ID': new_id_tournois +1,
        'tournament': new_tournois.name,
        'location': new_tournois.location,
        'date': new_tournois.date,
        'series':new_tournois.series,
        'surface':new_tournois.surface
    }
    nt=pd.DataFrame([new_tournois])
    nt['date']=pd.to_datetime(nt['date'])
    new_tournois_dum=pd.get_dummies(nt,columns=['series','surface'],prefix='',prefix_sep='')
    nt_tournois=tournois_df_dum.merge(new_tournois_dum,how='outer')
    tournois_df_dum=nt_tournois.fillna(0.0)
    tournois_db=tournois_df_dum.to_dict('records')

    return new_tournois_dum.to_dict('records')










@api.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    """
    Description:
    Cette route permet à un utilisateur de s'inscrire en fournissant les détails de l'utilisateur. Elle ajoute ensuite l'utilisateur à la liste des utilisateurs et renvoie un jeton JWT.

    Args:
    - user (UserSchema, Body): Les détails de l'utilisateur à créer.

    Returns:
    - str: Un jeton JWT si l'inscription est réussie.

    Raises:
    Aucune exception n'est levée.
    """

    users.append(user)
    return sign_jwt(user.username)


@api.post("/user/login", tags=["user"])
async def user_login(user: UserSchema = Body(...)):
    """
    Description:
    Cette route permet à un utilisateur de se connecter en fournissant les détails de connexion. Si les détails sont valides, elle renvoie un jeton JWT. Sinon, elle renvoie une erreur.

    Args:
    - user (UserSchema, Body): Les détails de connexion de l'utilisateur.

    Returns:
    - str: Un jeton JWT si la connexion réussit.

    Raises:
    - HTTPException(401, detail="Unauthorized"): Si les détails de connexion sont incorrects, une exception HTTP 401 Unauthorized est levée.
    """

    if check_user(user):
        return sign_jwt(user.email)
    return {"error": "Wrong login details!"}
