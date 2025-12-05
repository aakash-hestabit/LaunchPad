FROM node:lts-alpine3.23

COPY package*.json .
RUN npm i 
COPY .gitignore .
COPY  src ./src

CMD ["npm","start"]