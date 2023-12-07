import pickle
import joblib


def save_model_pickle(model, name):
    with open(name, 'wb') as f:
        pickle.dump(model, f)


def save_model_joblib(model, name):
    joblib.dump(model, name)


def load_model(path_pkl_model):
    return(joblib.load(path_pkl_model))