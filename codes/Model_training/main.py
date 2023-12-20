# Package

from data_loader import DataHandler
from utile import path_db, log_separator
from preprocessing import preprocess_data
from feature_eng import feature_eng

from model import LogisticRegressionHandler

#Init 
data_handler = DataHandler()

# 01 Import data
print('Lancement du code 01: data_loader.py')
#df = data_handler.load_data()
df = data_handler.read_from_volume()

print('taille du dataframe:', df.shape)
log_separator()

# 02 Preprocessing data
print('lancement du code 2: preprocessing.py')
test = preprocess_data(df)
print('output preprocess:', test.shape)
print('colonne names:', test.columns)
log_separator()

# 03 feature enginering
print('Lancement du code 3: feature_eng.py')
X_train, X_test, y_train, y_test = feature_eng(test)
print('shape', X_train.shape, 'shape_test:', X_test.shape)
log_separator()

# 04 modele training
print('Lancement du code 4: modele_training.py')
# Créer une instance de la classe LogisticRegressionHandler
logistic_regression_handler = LogisticRegressionHandler()
logistic_regression_handler.train_model(X_train, y_train)
log_separator()

# 05 prediction
y_pred = logistic_regression_handler.predict(X_test)
log_separator()

# 06 Evaluate model
print('Lancement du code 6: evaluate')
accuracy, confusion, classification_rep = logistic_regression_handler.evaluate(y_test, y_pred)
print(f"Précision du modèle : {accuracy}")
print("Matrice de confusion :")
print(confusion)
print("Rapport de classification :")
print(classification_rep)
log_separator()

# 07 model save
logistic_regression_handler.save_model_pickle('File_Data_Volume/atp_logistic_model.pkl')
logistic_regression_handler.save_model_pickle('File_Data_Volume/atp_logistic_model.joblib')
