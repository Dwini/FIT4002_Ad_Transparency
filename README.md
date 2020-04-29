# FIT4002_Ad_Transparency
Repository for a final year project at Monash University around ad transparency

## Insructions for running the `/test-docker-container` project as a docker file
1. Download and run the latest docker toolbox executable for your OS from [here](https://github.com/docker/toolbox/releases). Include VirtualBox and Kitematic if not already installed.
2. Run the Docker Quickstart Terminal. The first time this is run it will add configuration variables to the computer.
3. Confirm docker is working by typing the command: `docker run hello-world`
4. Install alpine with python by typing the command: `docker image pull python:3.7-alpine`
5. Open terminal in `/test-docker-container`.
6. Build docker image by running `docker build -t <image_name> .`. Where <image_name> is an arbitrary identifier you can set.
7. Run docker image in a container by running `docker run -t --rm --name <container_name> <image_name>`. Where <container_name> is an arbitrary identifier you can set. This container will be deleted once exited.
