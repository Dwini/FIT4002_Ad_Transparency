# define base image.
FROM python:3.7-slim-buster as base

# copy everything into /app and move into that directory.
COPY . /app
WORKDIR /app

# install all requirements with pip.
RUN python -m pip install --upgrade pip
RUN pip install --upgrade --no-cache-dir -r ./requirements.txt

# expose port 5000
EXPOSE 5000

# set the endpoint of the DB Project.
ENV DB_URI "http://127.0.0.1:8080"

# run flask server in gunicorn as it is a secure wsgi server.
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--workers=1", "--threads=256", "app:app"]
