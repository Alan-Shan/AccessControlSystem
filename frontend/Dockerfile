FROM node:12.18.2-alpine as frontend

ARG VUE_APP_URL
ENV VUE_APP_URL=$VUE_APP_URL
ARG VUE_API_URL
ENV VUE_API_URL=$VUE_API_URL
ARG VUE_AUTH_URL
ENV VUE_AUTH_URL=$VUE_AUTH_URL

WORKDIR .

COPY package.json ./

# install simple http server for serving static content
RUN npm install -g http-server

COPY . .

# build app for production with minification
RUN npm run build

EXPOSE 8080

CMD [ "http-server", "dist" ]
