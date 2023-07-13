#Download base image ubuntu 18.04
FROM python:3.7

ENV NB_USER jovyan
ENV NB_UID 1000
ENV HOME /home/${NB_USER}

RUN apt-get update && apt-get install -y \
    haveged \
    tar \
    wget \
    bash \
    rsync \
    gcc \
    libfreetype6-dev \
    libhdf5-serial-dev \
    libpng-dev \
    libzmq3-dev \
    python3 \
    python3-dev \
    python3-pip \
    unzip \
    pkg-config \
    software-properties-common \
    graphviz

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

# Install OpenJDK-11
RUN apt-get update && \
    apt-get install -y default-jre && \
    apt-get clean;

# Fix certificate issues
RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;
# Setup JAVA_HOME -- useful for docker commandline
#ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
#RUN export JAVA_HOME

#RUN echo "export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/" >> ~/.bashrc

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip3 install --upgrade pip
RUN pip3 install jupyter notebook==6.* numpy

RUN pip3 install crosslingual-coreference==0.2.3 spacy-transformers==1.1.5 wikipedia neo4j
RUN pip3 install --upgrade google-cloud-storage
RUN pip3 install transformers==4.18.0
RUN python3 -m spacy download en_core_web_sm

# Make sure the contents of our repo are in ${HOME}
#RUN mkdir -p /home/jovyan/tutorials
#RUN mkdir -p /home/jovyan/jupyter

RUN jupyter notebook --generate-config
#COPY jupyter_notebook_config.json /home/jovyan/.jupyter/jupyter_notebook_config.json
USER root
RUN chown -R ${NB_UID} ${HOME}
USER ${NB_USER}

WORKDIR ${HOME}

# Specify the default command to run
CMD ["jupyter", "notebook", "--ip", "0.0.0.0"]
