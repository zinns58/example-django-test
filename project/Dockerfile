# pull official base image
FROM python:3.7-alpine

# set arg value
ARG http_proxy
ARG https_proxy
ARG socks_proxy
ARG DJANGO_CONFIGURATION

# set work directory
WORKDIR /usr/src/app

# Set Environment Variable
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true

# Installing temporary packages required for installing requirements.pip
RUN apk add --no-cache \
    python3-dev \
    postgresql-dev \
    g++ \
    gcc \
    freetds-dev

# required, Pillow
RUN apk add --no-cache \
    jpeg-dev \
    zlib-dev

# copy project
COPY . /usr/src/app/

# install dependencies
# docker-compose 에서 설정한 DJANGO_CONFIGURATION 값을 사용
RUN pip install --upgrade pip
# COPY ./config/requirements /usr/src/app/config/requirements
RUN pip install --no-cache-dir -r /usr/src/app/config/requirements/${DJANGO_CONFIGURATION}.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# # run entrypoint.sh
ENTRYPOINT ["sh", "/usr/src/app/entrypoint.sh"]