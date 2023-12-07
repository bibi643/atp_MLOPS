FROM python:3.10.12

WORKDIR /ATP_API

COPY requirements.txt .
COPY ./src/api ./src/api
COPY ./src/data ./src/data
COPY ./src/model ./src/model
COPY ./src/user_admin ./src/user_admin
EXPOSE 8000




RUN pip install -r  requirements.txt

CMD ["python", "./src/api/main_api_V2.py"]



