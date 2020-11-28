FROM ubuntu:latest
COPY . /app
WORKDIR /app
RUN apt-get update -y && apt-get install -y python3-pip python3-dev build-essential git && pip3 install -r requirements.txt
EXPOSE 5000
CMD python3 manage.py runserver --host 0.0.0.0