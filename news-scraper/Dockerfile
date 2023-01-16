FROM python:3.9-alpine

WORKDIR /app 

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN crontab crontab

CMD ["crond", "-f"]
