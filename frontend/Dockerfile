# base image
FROM node:12.2.0-alpine
# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH
ARG VUE_APP_URL
ENV VUE_APP_URL=$VUE_APP_URL
ARG VUE_API_URL
ENV VUE_API_URL=$VUE_API_URL
ARG VUE_AUTH_URL
ENV VUE_AUTH_URL=$VUE_AUTH_URL

# install and cache app dependencies
COPY package.json /app/package.json
RUN npm install
RUN npm install @vue/cli@3.7.0 -g
COPY . .

# start app
CMD ["npm", "run", "serve"]