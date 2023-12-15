FROM node:21 AS build

WORKDIR /app
COPY package*.json ./

RUN npm install
COPY . .

RUN npm run build

FROM nginx

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Copy built files from into nginx
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]