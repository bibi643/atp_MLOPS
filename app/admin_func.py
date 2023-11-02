
#PACKAGES
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext



security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

admins= {

    "Julien": {
        "username": "Julien",
        "name": "Julien Datascientest",
        "hashed_password": pwd_context.hash('datascientest'),
    },

    "Benjamin" : {
        "username" :  "Benjamin",
        "name" : "Benjamin Datascientest",
        "hashed_password" : pwd_context.hash('datascientest'),
    },

    "Rui": {
        "username": "Rui",
        "name": "Rui Datascientest",
        "hashed_password": pwd_context.hash('datascientest'),
    },

    "Dimitri" : {
        "username" :  "Dimitri",
        "name" : "Dimitri Datascientest",
        "hashed_password" : pwd_context.hash('datascientest'),
    }

}



def get_current_admin(credentials: HTTPBasicCredentials = Depends(security)):
    """This function is to give access to certain part of the api to the different admins"""
    username = credentials.username
    if not(admins.get(username)) or not(pwd_context.verify(credentials.password, admins[username]['hashed_password'])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
