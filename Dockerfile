#FROM nvidia/cuda:12.0.0-devel-ubuntu22.04
FROM ubuntu:22.10

RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN python3 -m pip install --upgrade pip
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get -y install default-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y mupdf-tools

RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN git clone https://github.com/huggingface/transformers
RUN cd transformers && pip install .

ENV PYTHONUNBUFFERED 1
RUN ls