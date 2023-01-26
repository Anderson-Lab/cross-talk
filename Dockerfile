FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get install -y gcc
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN python3 -m pip install --upgrade pip

RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1
RUN ls