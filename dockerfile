FROM python:3.10.12-slim-buster

# Install Redis
RUN apt-get update && apt-get install -y redis-server

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

ENV PORT=8080

# Expose app port
EXPOSE $PORT

# Start app
CMD ["sh", "-c", "redis-server --daemonize yes && python main.py"]