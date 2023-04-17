# base image
FROM node:13.12.0-alpine as build-stage

# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH
ARG REACT_APP_URL
ENV REACT_APP_URL=$REACT_APP_URL
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL
ARG REACT_APP_AUTH_URL
ENV REACT_APP_AUTH_URL=$REACT_APP_AUTH_URL

# install and cache app dependencies

COPY package.json /app/package.json
COPY . .
RUN npm install --silent

RUN REACT_APP_URL=${REACT_APP_URL}
RUN REACT_APP_API_URL=${REACT_APP_API_URL}
RUN REACT_APP_AUTH_URL=${REACT_APP_AUTH_URL}

RUN npm install react-scripts@3.4.1 -g --silent

RUN npm run build

#CMD ["npm", "start"]

FROM nginx:1.19.1-alpine as production-stage

COPY --from=build-stage /app/build /usr/share/nginx/html

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx/nginx.conf /etc/nginx/conf.d

EXPOSE 80

CMD ["nginx", "-g", "daemon off;" ]
