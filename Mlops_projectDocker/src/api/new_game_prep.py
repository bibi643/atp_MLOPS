
from data_loader import load_data
from utile import path_db
from preprocessing import preprocess_data
from feature_eng import feature_eng
from modele import logistic_regression_model
from modele_training import train_logistic_regression_model
from modele_predict import accuracy_and_confusion_matrix
from model_save import save_model_pickle, save_model_joblib



#Import the data
# 01 Import data
print('Lancement du code 01: data_loader.py')
df_new_game = load_data(path_db)

#Select a random line
df_new_game=df_new_game.sample(1)
test_new_game= preprocess_data(df_new_game)


