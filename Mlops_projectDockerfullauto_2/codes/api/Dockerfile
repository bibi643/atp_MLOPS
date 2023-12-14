FROM python:3.10.12

WORKDIR /ATP_API


COPY . .
COPY requirements.txt .






RUN pip install -r  requirements.txt
EXPOSE 8000






CMD ["python", "main_api_V2.py"]



