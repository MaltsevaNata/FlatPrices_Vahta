FROM node:12-buster as build
WORKDIR /usr/app
COPY package.json .
RUN npm install

RUN npm install vue-socket.io --save
RUN npm install vue-socket.io-extended socket.io-client

COPY . .

RUN npm run build

FROM nginx:alpine as production
RUN apk add curl
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
COPY --from=build /usr/app/dist /usr/share/nginx/html