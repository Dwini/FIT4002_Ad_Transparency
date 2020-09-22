# Dashboard Project for Ad Transparency

## Deploy Locally
1. Run DB Project.
2. Install requirements with `pip install -r requirements.txt`. Do not worry if gunicorn does not install.
3. Run flask application with `python app.py`.

## Deploy in container
1. Move to `\dashboard` directory.
2. Build dashboard image with `docker build -t dash_image .`.
3. Run a dashboard container with `docker run -p 80:5000 dash_image`
4. As we are binding ports, ensure the container is deleted after closed. Check open containers with `docker ps -a`. Close container with `docker stop <container id>`.
5. Check the IP Address of the docker container to access the webserver: `docker-machine ip default`.
