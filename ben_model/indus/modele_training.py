from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def train_logistic_regression_model(X_train, X_test, y_train, y_test, model):
    
    # Normalisez les données en utilisant StandardScaler
    scaler = StandardScaler()
    #X_train = scaler.fit_transform(X_train)
    #X_test = scaler.transform(X_test)
    
    # Entraînez le modèle sur les données d'entraînement
    model.fit(X_train, y_train)
    
    # Prédiction 
    y_pred = model.predict(X_test)
    
    #accuracy = accuracy_score(y_test, y_pred)
    #classification_rep = classification_report(y_test, y_pred)
    
    return y_pred
