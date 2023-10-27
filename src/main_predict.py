# Package

from data_loader import load_data
from utile import path_db
from preprocessing import preprocess_data
from feature_eng import feature_eng, feature_eng_predict
from modele_predict import accuracy_and_confusion_matrix
from model_save import load_model


# 01 Import data
print('Lancement du code 01: data_loader.py')
df = load_data(path_db)\
    .sample(1)
    


# 02 Preprocessing data
print('lancement du code 2: preprocessing.py')
test = preprocess_data(df)
print('output preprocess:', test.shape)

#Select the player with API input
#test.query('p1_Name=={} and p2_Name={} and date ={}')



# 03 Feature_eng_predict
print('lancement du code 3: Feature_eng_predict.py')
x_new = feature_eng_predict(test)
print('Shape X_new', x_new.shape)


# 04 Load model

model = load_model('./atp_logistic_model.pkl')


# 05 predict new data

if model.predict(x_new.head(5))==1 :

    winner = '1'
    nom = test.p1_Name
    cote = test.p1_b365

else:
        
    winner = '2'
    nom = test.p2_Name
    cote = test.p2_b365



print('''
###################
Resultat du match :
Joueur {} gagne.
Il faut parier sur {}

La cote est de : {}

GROSSE COTE, GROS GAIN , GROS RESPECT !!!!!

L'abus de jeu d'argent est dangereux pour la santé (sauf si on gagne tout le temps)

'''.format(winner,nom,cote )
)