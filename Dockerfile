FROM node:18-slim

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

# Using a simple server to serve the build
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "3000"]
