FROM node:22-alpine
WORKDIR /web
COPY package.json .
RUN npm install --production
COPY index.html .
COPY server.js .
EXPOSE 5173
CMD ["npm","start"]
