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
RUN pip3 install -r requirements.txt

RUN git clone https://github.com/huggingface/transformers
RUN cd transformers && pip3 install .

ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
RUN pip3 install jupyter notebook==6.* numpy

RUN jupyter notebook --generate-config
#COPY jupyter_notebook_config.json /home/jovyan/.jupyter/jupyter_notebook_config.json
USER root
ENV NB_USER jovyan
ENV NB_UID 1000
ENV HOME /home/${NB_USER}
RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

WORKDIR ${HOME}

# Specify the default command to run
CMD ["jupyter", "notebook", "--ip", "0.0.0.0"]
