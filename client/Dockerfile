FROM node:18-alpine as install-step
WORKDIR /client
ENV PATH /client/node_modules/.bin:$PATH
COPY package.json package-lock.json ./
RUN npm ci
COPY tsconfig.json .env.production .env.development ./
COPY ./public ./public

FROM install-step as development
WORKDIR /client
VOLUME ./src
CMD ["npm", "run", "start"]

FROM install-step as build-step
WORKDIR /client
COPY ./src ./src
RUN npm run build

FROM nginx:stable-alpine as production
COPY --from=build-step /client/build /usr/share/nginx/html
COPY reverse-proxy/nginx.default.conf /etc/nginx/conf.d/default.conf
