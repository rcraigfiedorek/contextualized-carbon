FROM node:18-alpine as base

WORKDIR /client
ENV PATH /client/node_modules/.bin:$PATH
COPY package.json package-lock.json ./
RUN npm ci
COPY tsconfig.json ./
COPY ./src ./src
COPY ./public ./public
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build-step /client/build /usr/share/nginx/html
COPY reverse-proxy/nginx.default.conf /etc/nginx/conf.d/default.conf
