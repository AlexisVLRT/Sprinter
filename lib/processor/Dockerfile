FROM python:3.8

ENV APP_HOME /app
ENV PYTHONPATH /app
WORKDIR $APP_HOME

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-u", "lib/processor/entrypoint.py"]