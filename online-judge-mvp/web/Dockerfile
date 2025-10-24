FROM node:22-alpine
WORKDIR /web
COPY package.json .
RUN npm install --production
COPY server.js .
COPY public ./public
EXPOSE 5173
CMD ["npm","start"]
