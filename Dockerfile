# set base image (host OS)
#ARG APP_IMAGE= python:3.8.5

#FROM $APP_IMAGE AS base
FROM ubuntu:trusty
RUN sudo apt-get -y update
RUN sudo apt-get -y upgrade
#Update Sqlite
RUN sudo apt-get install -y sqlite3 libsqlite3-dev
#FROM base as builder
FROM  python:3.8.5
# set the working directory in the container
WORKDIR /Scala
# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . /Scala

#SETTING PORT
EXPOSE 5000

#Command to set app
#CMD ["export", " FLASK_APP=main.py"]
#RUN export FLASK_APP=main.py
#first command before runing
#CMD ["export", "FLASK_ENV=production"]
#RUN export FLASK_ENV=production
#second command before runing
#CMD ["FLASK_DEBUG=true"]
#RUN FLASK_DEBUG=true
# command to run on container start
#CMD ["export FLASK_APP=main.py", "export FLASK_ENV=production", "FLASK_DEBUG=false", "flask", "run"]

ENV FLASK_APP main.py
ENV FLASK_ENV production
ENV FLASK_DEBUG 0
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
