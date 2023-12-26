from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import joblib

class LogisticRegressionHandler:
    def __init__(self):
        self.model = LogisticRegression()

    def train_model(self, X_train, y_train):
        # Entraînez le modèle sur les données d'entraînement
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        # Prédiction
        y_pred = self.model.predict(X_test)
        return y_pred

    def evaluate(self, y_test, y_pred):
        # Calcul de l'accuracy
        accuracy = accuracy_score(y_test, y_pred)

        # Calcul de la matrice de confusion
        confusion = confusion_matrix(y_test, y_pred)

        # Calcul du rapport de classification
        class_report = classification_report(y_test, y_pred)

        return accuracy, confusion, class_report

    def save_model_pickle(self, name):
        with open(name, 'wb') as f:
            pickle.dump(self.model, f)

    def save_model_joblib(self, name):
        joblib.dump(self.model, name)

    def load_model(self, path_model):
        return joblib.load(path_model)
