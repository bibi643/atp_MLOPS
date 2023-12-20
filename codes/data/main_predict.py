# Package

from data_loader import load_data
from utile import path_db, log_separator
from preprocessing import preprocess_data
from feature_eng import feature_eng, feature_eng_predict
from model import LogisticRegressionHandler





# 01 Import data
print('Lancement du code 01: data_loader.py')
df = load_data(path_db)\
    .sample(1)
log_separator()

# 02 Preprocessing data
print('lancement du code 2: preprocessing.py')
test = preprocess_data(df)
print('output preprocess:', test.shape)
print('colonne names:', test.columns)
log_separator()

# 03 feature enginering
print('Lancement du code 3: feature_eng.py')
x_new = feature_eng_predict(test)
print('shape', x_new.shape)
log_separator()


# 04 Load model
logistic_regression_handler = LogisticRegressionHandler()


model = logistic_regression_handler.load_model('./atp_logistic_model.pkl')


# 05 predict new data

if model.predict(x_new.head(1))==1 :

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
