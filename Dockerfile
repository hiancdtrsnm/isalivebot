FROM python:3.8


RUN pip install pipenv

COPY . /app

WORKDIR /app

RUN pipenv install --system  --skip-lock

CMD python isalivebot.py