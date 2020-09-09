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
1. Ensure node dependencies are up to date by running `npm install` in `/db` directory.
2. Run `docker-compose up --build`. If node import error occurs, update the module locally and retry.

### Running the DB container individually.
1. With docker toolbox cmd still open. Open terminal in `/db` directory`.
2. Build the custom db docker image by running `docker build -t <image_name> .`. Where <image_name> is an arbitrary identifier you can set.
3. Run docker image in a container by running `docker run --rm <image_name>`. This container will be deleted once exited.

### Running the Bot container individually.
1. With docker toolbox cmd still open. Open terminal in `/bot` directory`.
2. Build the custom bot docker image by running `docker build -t <image_name> .`. Where <image_name> is an arbitrary identifier you can set.
3. Run docker image in a container by running `docker run --rm --env AD_USERNAME=<username> --env USE_PROXIES=<1/0> --env CHANGE_LOCATION=<1/0> <image_name>`. Where <username> is the username of the google profile to run in this container. This container will be deleted once exited.

### Helpfull commands in docker.
* Once a container is built, we can navigate as root with `docker run -it -rm <image_name> /bin/sh`.
* List all docker images with `docker images`
* Clear all old containers with `docker container prune`
* Confirm that the proxy addresses are working by running `python bot/ip_check.py`.

## Instructions for running project in AWS.
* See README.md in `/aws` directory.

TODO: Automate the process of generating `task-definition.json` file. Automate the running of tasks. Automate the stopping of tasks.

### Notes
* When db container is up, visit http://localhost:8080 to get database contents as JSON. Then for an improved table view use: [json2table](http://json2table.com/) or [JSON to CSV](https://json-csv.com/). If you just want to view db contents and not have bots running, use `docker-compose up --build db`
* To handle captcha:
- Make sure `./out` volume is enabled in `docker-compose.yml` and `out` folder is created in this directory
- Wait until "Captcha encountered!" shows up in console output
- Open `out/captcha.png` and create file `out/captcha` with the captcha text (single line, no spaces). Better to have this file ready, only 20 seconds to enter captcha.