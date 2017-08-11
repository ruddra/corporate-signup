FROM python:latest
ENV PYTHONUNBUFFERED 1

#ENV C_FORCE_ROOT true


RUN mkdir /config
RUN mkdir /static
ADD requirements.txt /config/
RUN pip install -r /config/requirements.txt

RUN mkdir /src
WORKDIR /src