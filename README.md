# FIT4002_Ad_Transparency
Repository for a final year project at Monash University around ad transparency

## Instructions for running the project in local
### DB Project
1. Install Node and npm.
2. Move to the `/db` directory and run `npm install` to install all dependencies.
3. Run project with `node index.js`.

### Bot Project
1. Download latest chromedriver executable from [here](https://sites.google.com/a/chromium.org/chromedriver/home).
2. Extract the chromedriver executable and place it in the default Selenium working director:
  - For Windows `C:\Windows`.
3. Install all python requirements by running `pip install --upgrade -r /requirements.txt`.
4. Ensure the DB Project is running.
5. run `set "AD_USERNAME=<username>" && set "USE_PROXIES=<1/0>" && set "CHANGE_LOCATION=<1/0>" && python bot/app.py`. Where <username> is the username of the google profile to run.

## Instructions for running the project in a docker container
### Installing Docker
1. Download and run the latest docker toolbox executable for your OS from [here](https://github.com/docker/toolbox/releases). Include VirtualBox and Kitematic if not already installed.
2. Run the Docker Quickstart Terminal. The first time this is run it will add configuration variables to the computer.
3. Confirm docker is working by typing the command: `docker run hello-world`

### Running the project
1. run `docker-compose up --build`

### Running the DB container individually.
1. With docker toolbox cmd still open. Open terminal in `/db` directory`.
2. Build the custom db docker image by running `docker build -t <image_name> .`. Where <image_name> is an arbitrary identifier you can set.
3. Run docker image in a container by running `docker run --rm <image_name>`. This container will be deleted once exited.

### Running the Bot container individually.
1. With docker toolbox cmd still open. Open terminal in `/bot` directory`.
2. Build the custom bot docker image by running `docker build -t <image_name> .`. Where <image_name> is an arbitrary identifier you can set.
3. Run docker image in a container by running `docker run --rm --env AD_USERNAME=<username> --env USE_PROXIES=<1/0> --env CHANGE_LOCATION=<1/0> <image_name>`. Where <username> is the username of the google profile to run in this container. This container will be deleted once exited.

### Helpfull commands in docker.
* Once a container is built, we can navigate as root with `docker run -it <container_name> /bin/sh`. Will not work if container is build with `--rm` as a parameter.
* Clear all old containers with `docker container prune`
* Confirm that the proxy addresses are working by running `python bot/ip_check.py`.

### New Notes
* Use `docker-compose up` to run the db and bot containers. You can still use the command above to navigate as root in each container (run `docker images` to get list of built images, most likely has the name *fit4002_ad_transparency_db* or *fit4002_ad_transparency_bot*)
* *USE_PROXIES* and *CHANGE_LOCATION* in bot/Dockerfile can be changed to enable proxies and location spoofing respectively (0 for off, 1 for on)
* When db container is up, visit *localhost:8080* to get database contents as json. Then for an improved table view use: [json2table](http://json2table.com/)
* For sharing files between container and host use `docker run --rm -it -v "<host_path>":<container_path> <container_name>`. This will attach the folder on the host at `<host_path>` to the folder inside the container at `<container_path>`. For windows `<host_path>` must be absolute, for example `C:\Users\<user>\VSCodeProjects\FIT4002_Ad_Transparency\src`
