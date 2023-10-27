from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def accuracy_and_confusion_matrix(y_test, y_pred):
    # Calcul de l'accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    # Calcul de la matrice de confusion
    confusion = confusion_matrix(y_test, y_pred)
    
    # Calcul du rapport de classification
    class_report = classification_report(y_test, y_pred)
    
    return accuracy, confusion, class_report






