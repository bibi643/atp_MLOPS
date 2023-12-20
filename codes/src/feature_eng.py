import numpy as np
import joblib

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import category_encoders as ce

#Problem
from utile import to_pandas

import joblib

def extract_date_components(df):
     '''
     bla bla bla doc function
     '''
     df['day'] = df['date'].dt.day
     df['month'] = df['date'].dt.month
     df['year'] = df['date'].dt.year
     
     return (df)



def pipeline_sklearn(df):

     '''
     bla bla bla
     '''
     # Sélectionner les colonnes catégorielles
     OHE_encoding = ['series', 'surface','round']
     LE_encoding = ['location','tournament']
     numerical_columns = df.select_dtypes(include='number').columns

     # Divisez les données en ensembles d'entraînement et de test
     X_train, X_test = train_test_split(df, test_size=0.2, random_state=42)

     # Créer un ColumnTransformer avec OneHotEncoder pour chaque colonne catégorielle
     preprocessor = ColumnTransformer(
     transformers=[
          ('freq', ce.CountEncoder(normalize=True),LE_encoding ), 
          ('OHE', OneHotEncoder(), OHE_encoding),
          ('num',StandardScaler(),numerical_columns) 
     ],
          remainder='passthrough'
     )

     # Appliquez la transformation aux ensembles d'entraînement et de test
     train_transformed = preprocessor.fit_transform(X_train)
     test_transformed = preprocessor.transform(X_test)
     
     #Return pandas data frame
     df_train_transformed = to_pandas(train_transformed, colnames=preprocessor.get_feature_names_out())
     df_test_transformed = to_pandas(test_transformed, colnames=preprocessor.get_feature_names_out())


     #Sava pipeline parameter

     # Enregistrez le pipeline complet dans un fichier
     joblib.dump(preprocessor, 'preprocessor_pipeline.pkl')




     return(df_train_transformed, df_test_transformed)


def create_intput_model(df):
     
     '''
     Bla bla bla
     '''

     temp_df = df\
          .assign(p1_won = np.where(df['remainder__p1_Name']==df['remainder__winner'],1,0))\
               .drop(['remainder__p2_Name'
                      ,'remainder__p1_Name'
                      ,'remainder__winner'
                      ,'remainder__date']
                      , axis = 1
                      )
     
     # Split les données en caractéristiques (X) et la variable cible (y)
     X = temp_df.drop(columns=['p1_won'])
     y = temp_df['p1_won']

     return(X, y)




def feature_eng(df):
    '''
    bla bla bla 
    '''
    # Extraction des composants de la date
    df = extract_date_components(df)

    # Transformation des caractéristiques avec sklearn
    df_train, df_test = pipeline_sklearn(df)

    # Création des données d'entrée du modèle
    X_train, y_train = create_intput_model(df_train)
    X_test, y_test = create_intput_model(df_test)

    return  (X_train, X_test, y_train, y_test)


def feature_eng_predict(df):

     '''
     bla bla bla 
     '''
     # Extraction des composants de la date
     df = extract_date_components(df)

     preprocessor_loaded = joblib.load('./preprocessor_pipeline.pkl')
     #Appliquer sklearn pipeline a df
     array_preprocessor = preprocessor_loaded.transform(df)

     #Return pandas data frame
     df_new = to_pandas(array_preprocessor, colnames=preprocessor_loaded.get_feature_names_out())

     # Nouvelle donnees a predire
     ## Il faut retirer y_new pour la vraie prod
     X_new, y_new = create_intput_model(df_new)

     return(X_new)
