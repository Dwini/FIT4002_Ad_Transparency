# FIT4002_Ad_Transparency
Repository for a final year project at Monash University around ad transparency

## Running `/test-docker-container` project

### Instructions for running the `/test-docker-container` project in local
1. Download latest chromedriver executable from [here](https://sites.google.com/a/chromium.org/chromedriver/home).
2. Extract the chromedriver executable and place it in the default Selenium working director:
  - For Windows `C:\Windows`.
3. Install all python requirements by running `pip install --upgrade -r /requirements.txt`.
4. run `main.py` with `python src/webscraper.py`. This will not run the project behind a proxy, so it should print your local IP Address.

### Instructions for running the `/test-docker-container` project in a docker container behind a proxy
1. Download and run the latest docker toolbox executable for your OS from [here](https://github.com/docker/toolbox/releases). Include VirtualBox and Kitematic if not already installed.
2. Run the Docker Quickstart Terminal. The first time this is run it will add configuration variables to the computer.
3. Confirm docker is working by typing the command: `docker run hello-world`
5. With docker toolbox cmd still open. Open terminal in `/test-docker-container`.
6. Build our custom docker image by running `docker build -t <image_name> .`. Where <image_name> is an arbitrary identifier you can set.
7. Run docker image in a container by running `docker run -t --rm --name <container_name> <image_name>`. Where <container_name> is an arbitrary identifier you can set. This container will be deleted once exited. This will print the IP Address of the container through both the HTTP_PROXY and HTTPS_PROXY.

### How to download HTTP_PROXY and HTTPS_PROXY lists
These proxy lists are supposedly updated every five minutes.
* [HTTP_PROXY](https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=US&ssl=all&anonymity=elite)
* [HTTPS_PROXY](https://api.proxyscrape.com/?request=getproxies&proxytype=https&timeout=10000&country=US&ssl=all&anonymity=elite)

TODO: Download new proxy list during build stage and choose random proxy.

### Helpfull commands in docker.
* Once a container is built, we can navigate as root with `docker run -it <container_name> /bin/sh`. WIll not work if container is build with `--rm` as a parameter.
* Confirm that the proxy addresses are working by running `python app/ip_check.py`.

### New Notes
* Use `docker-compose up` to run the db and bot containers. You still use the command above to navigate as root in each container (run `docker images` to get list of built images, most likely has the name *fit4002_ad_transparency_db* or *fit4002_ad_transparency_bot*)
* *USE_PROXIES* and *CHANGE_LOCATION* in bot/Dockerfile can be changed to enable proxies and location spoofing respectively (*0* for off, *1* for on)
* When db container is up, visit *localhost:8080/<table_name>* to get list of items stored in a table (assuming db running on port 8080). For example *localhost:8080/ads* will retrieve a list of all items in 'Ads' table in DynamoDB as json. Then for an improved table view use: [json2table](http://json2table.com/)