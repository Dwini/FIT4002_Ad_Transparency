# define base image.
FROM alpine:latest as base

#####

## start builder stage.

# this is the first stage of the build.
# it will install all requirements.
FROM base as builder

# Installs latest Chromium package.
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" > /etc/apk/repositories
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories

# update installers.
RUN apk update

# install all package requirements.
RUN apk add --upgrade apk-tools python3 py-pip chromium chromium-chromedriver

# copy the python requirements file into the install directory and install all python requirements.
COPY requirements.txt /requirements.txt
RUN pip install --upgrade -r /requirements.txt

# copy the source code into /app and move into that directory.
COPY src /app

## end builder stage.

#####

## start base stage.

# this is the image this is run.
FROM builder

# set the proxy addresses
ENV HTTP_PROXY "http://12.139.101.100:80"
ENV HTTPS_PROXY "https://13.59.138.149:80"

# default entry point.
CMD ["python3", "app/main.py"]
## end base stage.
