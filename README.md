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

## Instructions for updating the project in AWS (ony Matt at the moment)
1. Install AWS CLI.
2. Get updated AWS credentials from [here](https://labs.vocareum.com/main/main.php).
3. Locally build bot and db images separately and push to docker hub.
  * bot image: `mattbertoncello/ad_transparency_bot`.
  * db image: `mattbertoncello/ad_transparency_db`.
4. Update the `task-definition.json` file to include the bot usernames in this batch. The db container must be specified.
5. Run the following command in root directory to define new task `aws ecs register-task-definition --cli-input-json file://task-definition.json`.
6. Login to AWS console and run the newly defined task.

TODO: Automate the process of generating `task-definition.json` file. Automate the running of tasks. Automate the stopping of tasks.

### Notes
* *USE_PROXIES* and *CHANGE_LOCATION* in `docker-compose.yml` can be changed to enable proxies and location spoofing respectively (0 for off, 1 for on)
* When db container is up, visit http://localhost:8080 to get database contents as JSON. Then for an improved table view use: [json2table](http://json2table.com/) or [JSON to CSV](https://json-csv.com/). If you just want to view db contents and not have bots running, use `docker-compose up --build db`
* For bypassing login captcha the above `docker-compose` commands won't work as there are problems with capturing input from the console. Follow these instructions instead:
  - Create an empty `temp` folder inside this directory
  - Make sure the *volumes* section is uncommented in `docker-compose.yml`
  - Build: `docker-compose build`
  - Spin up db container if not currently running: `docker-compose up db`
  - Run bot container: `docker-compose run bot`
  - If captcha is encountered a screenshot that includes the captcha image will be saved under `temp/captcha.png`. Enter the captcha text into the console and continue