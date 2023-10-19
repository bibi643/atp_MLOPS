#Package

from data_loader import load_data
from utile import path_db
from preprocessing import preprocess_data
from feature_eng import feature_eng
from modele import logistic_regression_model
from modele_training import train_logistic_regression_model
from modele_predict import accuracy_and_confusion_matrix


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

#04 modele
print('Lancement du code 4: modele.py')
logistic_model = logistic_regression_model()
print("modele : ", logistic_model)

#05 modele training
print('Lancement du code 5: modele_training.py')
y_pred = train_logistic_regression_model(X_train, X_test, y_train, y_test, logistic_model)
print('shape pred: ', y_pred.shape)

#06 modele predict
print('Lancement du code 6: modele_predict.py')
accuracy, confusion, classification_rep = accuracy_and_confusion_matrix(y_test, y_pred)
print(f"Précision du modèle : {accuracy}")
print("Matrice de confusion :")
print(confusion)
print("Rapport de classification :")
print(classification_rep)