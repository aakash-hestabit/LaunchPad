# Stage 1
FROM node:lts-alpine3.23 AS build

RUN  apk add --no-cache curl

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
