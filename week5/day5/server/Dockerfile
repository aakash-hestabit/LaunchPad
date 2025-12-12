FROM node:lts-alpine3.23

RUN  apk add --no-cache curl

WORKDIR app/

COPY package*.json .

RUN npm install 

COPY . .

EXPOSE 5000

CMD ["npm" , "start"]