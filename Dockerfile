# base image
FROM python:3

# env variables
ENV PYTHONUNBUFFERED 1

# work directory
RUN mkdir /flask
WORKDIR /flask

# project requirements
RUN pip install --upgrade pip
COPY /flask/requirements.txt /flask/
RUN pip install -r /flask/requirements.txt

# app
COPY . /flask/