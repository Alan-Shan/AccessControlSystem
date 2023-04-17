# base image
FROM node:12.2.0-alpine as build-stage

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH
ARG REACT_APP_URL
ENV REACT_APP_URL=$REACT_APP_URL
ARG REACT_API_URL
ENV REACT_API_URL=$REACT_API_URL
ARG REACT_AUTH_URL
ENV REACT_AUTH_URL=$REACT_AUTH_URL

# install and cache app dependencies

COPY package.json /app/package.json
COPY . .
RUN npm install

RUN npm run build

FROM nginx:1.19.1-alpine as production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx/nginx.conf /etc/nginx/conf.d

EXPOSE 80

CMD ["nginx", "-g", "daemon off;" ]
