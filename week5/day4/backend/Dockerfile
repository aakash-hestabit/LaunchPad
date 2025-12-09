FROM node:lts-alpine3.23

WORKDIR app/

COPY package*.json .

RUN npm install 

COPY src/ /app/src

EXPOSE 5000

CMD ["npm" , "start"]