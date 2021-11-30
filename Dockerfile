FROM python:3.9

COPY . /app
WORKDIR /app/deploy

RUN pip install -r requirements.txt

WORKDIR /app

EXPOSE 8081
CMD ["python3", "application.py"]