from data_loader import DataHandler

import pytest
import pandas as pd
import os

def test_load_data():

    data_handler = DataHandler()
    #Load data
    df_csv = data_handler.load_data(type='csv')
    #Load new data
    df_excel = data_handler.load_data(type='excel')
    # Vérifie que le DataFrame n'est pas vide
    assert not df_csv.empty
    assert not df_excel.empty

    #Plus d'une colonne
    assert df_csv.shape[1] >1
    assert df_excel.shape[1] >1
 
    # Vérifie que le DataFrame est une instance de pandas DataFrame
    assert isinstance(df_csv, pd.DataFrame)
    assert isinstance(df_excel, pd.DataFrame)

def test_columns_names():

    raw_features = ['ATP', 'Location', 'Tournament', 'Date', 'Series', 'Court', 'Surface',
                'Round', 'Best of', 'Winner', 'Loser', 'WRank', 'LRank', 'Wsets',
                'Lsets', 'Comment', 'PSW', 'PSL', 'B365W', 'B365L'] 

    data_handler = DataHandler()

    df = data_handler.load_data(type='csv')\
                     .drop(['elo_winner','elo_loser','proba_elo'],axis=1)\
                        .assign(Date=lambda x: pd.to_datetime(x['Date'], format='%Y-%m-%d'))

    new_data = data_handler.load_data(type='excel')\
                        .loc[:,raw_features]
    
    assert set(df.columns) == set(new_data.columns)