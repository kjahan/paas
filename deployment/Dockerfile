FROM continuumio/miniconda3
RUN apt-get update
RUN apt-get install vim -y

WORKDIR /opt

RUN mkdir -p paas/uploads
RUN mkdir -p paas/figs
COPY server.py paas/
COPY environment.yml paas/

# Create the environment:
RUN conda env create -f paas/environment.yml