# define base image.
FROM python:3.7-alpine as base

#####

## start builder stage.

# this is the first stage of the build.
# it will install all python requirements.
FROM base as builder

# create directory at root called 'install'. move to this directory.
RUN mkdir /install
WORKDIR /install

# update installers.
RUN apk update && \
  pip install --upgrade pip

# copy the requirements file into the install directory and install all requirements.
COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install --no-warn-script-location -r /requirements.txt

## end builder stage.

#####

## start base stage.

# this is the image this is run.
FROM base

# import the installed files from the builder image into /user/local.
COPY --from=builder /install /usr/local

# copy the source code into /app and move into that directory.
COPY src /app
#WORKDIR /app

# default entry point.
CMD ["python", "app/main.py"]

## end base stage.
