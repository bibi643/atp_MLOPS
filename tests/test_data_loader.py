from src.data_loader import load_data
from src.preprocessing import preprocess_data
from src.model import LogisticRegressionHandler

import pytest
import pandas as pd
import os

# Fixture pour charger la première ligne du fichier CSV
@pytest.fixture
def sample_data_csv():
    csv_data = """ATP,Location,Tournament,Date,Series,Court,Surface,Round,Best of,Winner,Loser,WRank,LRank,Wsets,Lsets,Comment,PSW,PSL,B365W,B365L,elo_winner,elo_loser,proba_elo
                    34,Queens Club,AEGON Championships,2012-06-16,ATP250,Outdoor,Grass,Semifinals,3,Nalbandian D.,Dimitrov G.,39,72,2.0,0.0,Completed,2.24,1.75,2.0,1.72,1819.330041538929,1699.959129885806,0.6653335666091081"""

    # Écrire la première ligne dans un fichier CSV temporaire
    csv_file_path = os.path.expanduser('~') + "/sample_data.csv"
    with open(csv_file_path, 'w', newline='') as file:
        file.write(csv_data)

    # Renvoyer le chemin du fichier CSV
    return csv_file_path


def test_load_data(sample_data_csv):
    # Utilise le fichier CSV de test en tant que fixture
    df = load_data(sample_data_csv)

    # Vérifie que le DataFrame n'est pas vide
    assert not df.empty

    #Plus d'une colonne
    assert df.shape[1] >1
 
    # Vérifie que le DataFrame est une instance de pandas DataFrame
    assert isinstance(df, pd.DataFrame)


def test_preprocess_data(sample_data_csv ):

    df = load_data(sample_data_csv)

    col_post_preprocessing = ['location', 'tournament', 'date', 'series', 'surface', 'round',
                              'best_of', 'proba_elo', 'winner', 'p1_Name', 'p1_b365', 'p1_elo',
                              'p1_rank', 'p2_Name', 'p2_b365', 'p2_elo', 'p2_rank'
                              ]
    

    data = preprocess_data(df)

    #nombre de colonnes fixées à 17 après le preprocessing
    assert data.shape[1] == 17

    #La liste des colonnes doit toujours être la même
    assert all(data.columns == col_post_preprocessing)


import pytest
from your_model_module import train_model, evaluate_model

