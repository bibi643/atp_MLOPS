#Package

from data_loader import load_data
from utile import path_db
from preprocessing import preprocess_data
from feature_eng import feature_eng

#01 Import data
print('Lancement du code 01: data_loader.py')
df = load_data(path_db)
print('taille du dataframe:' , df.shape)

#02 Preprocessing data
print('lancement du code 2: preprocessing.py')
test = preprocess_data(df)
print('output preprocess:', test.shape)
print('colonne names:', test.columns)

#03 feature enginering 
print('Lancement du code 3: feature_eng.py')
X_train, X_test, y_train, y_test = feature_eng(test)
print('shape',X_train.shape, 'shape_test:', X_test.shape)