# define base image.
FROM python:3.7-slim-buster as base

#####

## start builder stage.

# this is the first stage of the build.
# it will install all requirements.
FROM base as builder

# upgrade pip.
RUN python -m pip install --upgrade pip

# Install Firefox dependencies
RUN apt-get update && \
  apt-get install -y --no-install-recommends --no-install-suggests libgtk-3.0 libdbus-glib-1-2 libx11-xcb1 libxt6 wget bzip2 gcc g++ xvfb curl

# Install Firefox
ARG FIREFOX_VERSION=81.0.1
RUN wget -q -O - "https://download.mozilla.org/?product=firefox-$FIREFOX_VERSION&os=linux64"  | tar -xj -C /opt && \
  ln -s /opt/firefox/firefox /usr/bin/

# Install Geckodriver
# ARG GECKODRIVER_VERSION=v0.27.0
# RUN wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
#   tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
#   chmod +x /usr/local/bin/geckodriver && \
#   rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

# Clean up Firefox dependencies
RUN apt-get purge -y --auto-remove bzip2 gcc g++

# copy the python requirements file into the install directory and install all python requirements.
COPY requirements.txt /requirements.txt
RUN pip install --upgrade --no-cache-dir -r /requirements.txt
RUN rm /requirements.txt 
# remove requirements file from container.

# copy the source code into /app and move into that directory.
COPY . /app

## end builder stage.

#####

## start base stage.

# this is the image this is run.
FROM builder

WORKDIR /app

# Create non-root user (for driver execution)
RUN useradd -ms /bin/bash bot && \
  chown -R bot:bot /app && \
  chmod 755 /app
USER bot

# default entry point. Container will force close after 1 minute.
CMD ["timeout", "--signal=SIGALRM", "15m", "python", "app.py", "-c"]
## end base stage.
