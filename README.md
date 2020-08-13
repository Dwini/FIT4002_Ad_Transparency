# FIT4002_Ad_Transparency
Repository for a final year project at Monash University around ad transparency

## Running `/test-docker-container` project

### Instructions for running the project in local
1. Download latest chromedriver executable from [here](https://sites.google.com/a/chromium.org/chromedriver/home).
2. Extract the chromedriver executable and place it in the default Selenium working director:
  - For Windows `C:\Windows`.
3. Install all python requirements by running `pip install --upgrade -r /requirements.txt`.
4. run `set "AD_USERNAME=<username>" && python src/app.py`. Where <username> is the username of the google profile to run.

### Instructions for running the `/test-docker-container` project in a docker container behind a proxy
1. Download and run the latest docker toolbox executable for your OS from [here](https://github.com/docker/toolbox/releases). Include VirtualBox and Kitematic if not already installed.
2. Run the Docker Quickstart Terminal. The first time this is run it will add configuration variables to the computer.
3. Confirm docker is working by typing the command: `docker run hello-world`
5. With docker toolbox cmd still open. Open terminal in `/test-docker-container`.
6. Build our custom docker image by running `docker build -t <image_name> .`. Where <image_name> is an arbitrary identifier you can set.
7. Run docker image in a container by running `docker run --rm --env AD_USERNAME=<username> <image_name>`. Where <username> is the username of the google profile to run in this container. This container will be deleted once exited.

### How to download HTTP_PROXY and HTTPS_PROXY lists
These proxy lists are supposedly updated every five minutes.
* [HTTP_PROXY](https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=US&ssl=all&anonymity=elite)
* [HTTPS_PROXY](https://api.proxyscrape.com/?request=getproxies&proxytype=https&timeout=10000&country=US&ssl=all&anonymity=elite)

### Helpfull commands in docker.
* Once a container is built, we can navigate as root with `docker run -it <container_name> /bin/sh`. Will not work if container is build with `--rm` as a parameter.
* Confirm that the proxy addresses are working by running `python app/ip_check.py`.
