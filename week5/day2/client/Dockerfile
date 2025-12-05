# Stage 1
FROM FROM node:lts-alpine3.23 AS build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

# Stage 2

FROM FROM node:lts-alpine3.23

WORKDIR /app

COPY package*.json ./

RUN npm install --omit=dev

COPY --from=build /app/dist /app/dist

EXPOSE 3000

CMD ["npm", "start"]
