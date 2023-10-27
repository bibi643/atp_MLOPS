


"""Project MLOps DataScientest
Remember you are in VENV environment so if you need new packaages. Have to be install in the terminal here."""

from fastapi import FastAPI

api= FastAPI()

@api.get('/')
def get_greetings():
    return "Bonjour cher parieur."

