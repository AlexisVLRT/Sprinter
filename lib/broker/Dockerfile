FROM python:3.8

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH /app

CMD ["python", "-u", "lib/broker/broker.py"]