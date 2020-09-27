FROM node:alpine

WORKDIR /usr/src/app

COPY ./package*.json ./
RUN npm install

COPY . .

EXPOSE 8080

# container will force close after 1 minute.
CMD [ "npm", "start" ]
