import sys 

from src.data_loader import load_data
from src.utile import path_db, log_separator, target, keeping_col, to_pandas
from src.preprocessing import preprocess_data
from src.feature_eng import feature_eng

from src.model import LogisticRegressionHandler
from sklearn.metrics import accuracy_score




def test_model():
    """
    On suppose qu'un monitoring de modèle à lancer un reentrainement
    """

    # 01 Import data
    print('Lancement du code 01: data_loader.py')
    df = load_data(path_db).sample(10000)  #Sample pour simuler nouvelle donnees
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

    logistic_regression_handler = LogisticRegressionHandler()
    # Train the model initially
    logistic_regression_handler.train_model(X_train, y_train)
    
    # Predict
    y_pred = logistic_regression_handler.predict(X_test)

    # Evaluate

    accuracy_after, confusion, classification_rep = logistic_regression_handler.evaluate(y_test, y_pred)
    
    
    # Baseline model

    base_model = logistic_regression_handler.load_model('./atp_logistic_model.pkl')

    base_y_pred = base_model.predict(X_test)

    accuracy_before = accuracy_score(y_pred=base_y_pred, y_true=y_test)
    
    # Check if the performance has improved

    assert accuracy_after > accuracy_before, f"Accuracy did not improve. Before: {accuracy_before}, After: {accuracy_after}"

