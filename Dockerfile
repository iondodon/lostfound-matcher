FROM python:3.9.12-buster

WORKDIR /lostfound-matcher

COPY . .

RUN apt update && apt install -y git
RUN pip install -r requirements.txt

EXPOSE 5000

CMD python ./src/app.py