# FIT4002_Ad_Transparency
Repository for a final year project at Monash University around ad transparency

## Prerequisites
1. Create `.env` file under `bot` directory with proper environment variables set. See `bot/.env.default` for an example.

## Instructions for running the project in local
### DB Project
1. Install Node and npm.
2. Move to the `/db` directory and run `npm install` to install all dependencies.
3. Run project with `npm start`.

### Bot Project
1. Move to the `/bot` directory and install all python requirements by running `pip install --upgrade -r requirements.txt`.
2. Make sure the correct `chromedriver` is being used. See `bot/driver/driver.py` and look for `CHROMEDRIVER_PATH`
2. Ensure the DB Project is running.
3. run `set "AD_USERNAME=<username>" && set "USE_PROXIES=0" && set "CHANGE_LOCATION=1" && set "NUM_TERMS=2" && set "DB_URL=http://localhost:8080" && set "UPLOAD_LOGS=0" && python app.py`. Where <username> is the username of the google profile to run.

## Instructions for running the project in a docker container
### Installing Docker
1. Download and run the latest docker toolbox executable for your OS from [here](https://github.com/docker/toolbox/releases). Include VirtualBox and Kitematic if not already installed.
2. Run the Docker Quickstart Terminal. The first time this is run it will add configuration variables to the computer.
3. Confirm docker is working by typing the command: `docker run hello-world`

### Running the project
1. Ensure node dependencies are up to date by running `npm install` in `/db` directory.
2. Ensure the correct bot is being used through the `AD_USERNAME` environment variable in `docker-compose.yml`
3. Run `docker-compose up --build`. If node import error occurs, update the module locally and retry.

### Running the DB container individually.
1. With docker toolbox cmd still open. Open terminal in `/db` directory`.
2. Build the custom db docker image by running `docker build -t <image_name> .`. Where <image_name> is an arbitrary identifier you can set.
3. Run docker image in a container by running `docker run --rm <image_name>`. This container will be deleted once exited.

### Running the Bot container individually.
1. With docker toolbox cmd still open. Open terminal in `/bot` directory`.
2. Build the custom bot docker image by running `docker build -t <image_name> .`. Where <image_name> is an arbitrary identifier you can set.
3. Run docker image in a container by running `docker run --rm --env AD_USERNAME=<username> <image_name>`. Where <username> is the username of the google profile to run in this container. This container will be deleted once exited.

### Helpfull commands in docker.
* Once a container is built, we can navigate as root with `docker run -it -rm <image_name> /bin/sh`.
* List all docker images with `docker images`
* Clear all old containers with `docker container prune`
* Confirm that the proxy addresses are working by running `python bot/ip_check.py`.

## Instructions for running project in AWS.
* See README.md in `/aws` directory.

TODO: Automate the process of generating `task-definition.json` file. Automate the running of tasks. Automate the stopping of tasks.

### Notes
* When db container is up, visit http://localhost:8080 to get database contents as JSON. Then for an improved table view use: [json2table](http://json2table.com/) or [JSON to CSV](https://json-csv.com/).
* To handle captcha:
- Create file `bot/out/captcha`, this is where you should enter the text for the captcha
- Wait until "Captcha encountered!" shows up in console output
- Open `bot/out/captcha.png` and edit `bot/out/captcha` with the captcha text (single line, no spaces). You are only given 20 seconds to enter captcha so better to have these files already open.
* Session data:
- Each bots session data is saved under `bot/out/sessions/<BOT_USERNAME>`
- If session data worked correctly `bot/out/login_proof.png` will be created
