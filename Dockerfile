# define base image.
FROM python:3.7-slim-buster as base

#####

## start builder stage.

# this is the first stage of the build.
# it will install all requirements.
FROM base as builder

# install all packages for chromedriver: https://gist.github.com/varyonic/dea40abcf3dd891d204ef235c6e8dd79.
RUN apt-get update && \
    apt-get install -y xvfb gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /chromedriver

# make the chromedriver executable and move it to default selenium path.
RUN chmod +x /chromedriver/chromedriver
RUN mv /chromedriver/chromedriver /usr/bin/chromedriver

# copy the python requirements file into the install directory and install all python requirements.
COPY requirements.txt /requirements.txt
RUN pip install --upgrade --no-cache-dir -r /requirements.txt
RUN rm /requirements.txt # remove requirements file from container.

# copy the source code into /app and move into that directory.
COPY src /app

## end builder stage.

#####

## start base stage.

# this is the image this is run.
FROM builder

# set the proxy addresses
#ENV HTTP_PROXY "http://64.227.126.52:3128"
#ENV HTTPS_PROXY "https://65.18.118.8:8080"

# default entry point.
CMD ["python", "app/webscraper.py", "-c"]
## end base stage.
