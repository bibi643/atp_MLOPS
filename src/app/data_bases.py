

#IMPORT THE PACKAGES
import pandas as pd
#from data_loader import load_data
from data_loader import DataHandler

from preprocessing import preprocess_data

#LOAD THE DATA
def data_preprocessed():
    data_handler = DataHandler()
    df= data_handler.read_from_volume()
    #df=load_data('atp_data.csv')
    df_preprocessed=preprocess_data(df)
    return df_preprocessed



#LOAD THE DATA
def player_df_db():
    data_handler = DataHandler()
    df= data_handler.read_from_volume()
    #df=load_data('atp_data.csv')
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
    player_base_updated_df=player_base_updated.reset_index()
    player_base_updated_df['Player_name']=player_base_updated_df['Player_name'].str.strip()
    player_base_updated_df=player_base_updated_df.sort_values(by=['Player_name'])
    player_base_updated_db= player_base_updated_df.to_dict('records')
    return player_base_updated_df,player_base_updated_db



def tournois_df_db():
    data_handler = DataHandler()
    df= data_handler.read_from_volume()
    #df=load_data('atp_data.csv')
    df_preprocessed=preprocess_data(df)
    tournois_df=df_preprocessed[['location','date','tournament','series','surface']]
    tournois_df=tournois_df.groupby(by=['tournament']).first()
    tournois_df=tournois_df.reset_index().reset_index().rename(columns={'index':'Tournois_ID'})
    tournois_df['Tournois_ID']=tournois_df['Tournois_ID']+1
    tournois_df['tournament']=tournois_df['tournament'].str.upper()

    #ici les characteristiques du tournoi sont dummifiees. Sans doute utile lorsque le user choisira deux joueru maia aussi le nom du tournoi.
    tournois_df_dum=pd.get_dummies(tournois_df,columns=['series','surface'],prefix='',prefix_sep='')
    tournois_db=tournois_df_dum.to_dict('records')
    return tournois_df,tournois_db

