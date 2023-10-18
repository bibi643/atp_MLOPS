# Comment lancer les codes .py

Compiler les les scripts pour générer X_train, X_test, y_train, y_test

```shell
#Installation du requirements sur le venv

#Activer le venv
source chemin_mon_venv/bin/activate
#Installer les packages
pip install -r requirements.txt

#Lancer les scripts, attention il faut tous les scripts dans le même répertoire.
export py= ...my_env/bin/python3

#On fait un flux de redirection faire une log
$py main.py > log.txt
```

# Preco arbo projet pour la suite 

```shell
bet_tennis/
│
├── data/
│   ├── raw/
│   ├── processed/
│
├── src/
│   ├── data/
│   │   ├── data_loader.py
│   │   ├── data_preprocessing.py
        |── Feature_engineering.py
│   │
│   ├── models/
│   │   ├── model.py
│   │   ├── model_training.py
|   |   |── model_predict.py
│   │
│   ├── evaluation/
│   │   ├── evaluate_model.py
│
├── config/
│   ├── config.yaml
│
├── notebooks/
│   ├── data_exploration.ipynb
│   ├── model_prototyping.ipynb
│
├── requirements.txt
│
├── README.md
```
Il reste à faire la partie model.py & model_training.py model.predict.py @Rui

POur la partie evaluate_model.py c'est à toi de jouer @Julien

A voir ce que tu juges le plus pertinent pour évaluer la qualité d'un modèle qui prédit la victoire d'un joueur de tennis.
Attention, tu ne sais pas encore le modèle exacte que @Rui va te transmettre, tes codes doivent s'adapter à n'importe quel modèle.
Tu sais juste qu'il s'agit d'une classification binaire.



