# Skrapbuk Christmas (Artwork trading Secret Santa)
![image](https://github.com/not-nic/skrapbuk-christmas/assets/67616855/39be3c6f-9e44-454b-9b1b-1bc814763b10)![image](https://github.com/not-nic/skrapbuk-christmas/assets/67616855/a4bb2db8-f73f-48a1-91ea-2a83d73bd0be)
## Project Description
This is a artwork trading Secret Santa project developed for the Gom's Garden discord sever, but can be adapted to work in your own Discord server. The application leverages discord OAuth to allow users to sign up to the 'event' which can then be started at a later date. 

Once an event has been started, each user is assigned a recipient or 'partner', where they are given information about the user which can be used as inspiration to create some artwork to upload. 

However, if this is used within personal / smaller communities, you could leverage the sign-up & questions process to give each other gift ideas, creating a traditional Secret Santa. This can be done by editing [Questions.vue](https://github.com/not-nic/skrapbuk-christmas/blob/master/src/views/Questions.vue) and rebuilding the application. 

### Tech Stack
I used Flask for the backend with the Flask-Discord library to facilitate discord OAuth. In addition, I used MySQL for the database and Vue.js for the frontend.

## How to Use
I've created a simplified flowchart to show how a user takes part in the skrapbuk event, and what the backend (Flask) is doing 'behind the scenes'. ![image](https://github.com/not-nic/skrapbuk-christmas/assets/67616855/c6fcb8de-19b2-4b7a-b737-0e7c11a2d283)*Note: Admin's are defined in the `config.yml` instead of users with admin privileges on a discord server.*

## Install Guide
1. **Prerequisites**: To use Discord's OAuth you will need to create an application [here](https://discord.com/developers/), from this you will need your application's:
	- Client ID
	- Client Secret
	- Bot Token

	These are needed for the following environment variables:
	```bash
	SB_CLIENT_ID = YOUR_CLIENT_ID_HERE
	SB_CLIENT_SECRET = YOUR_CLIENT_SECRET_HERE
	SB_BOT_TOKEN = YOUR_BOT_TOKEN_HERE
	```
2. Clone this repository on your machine using the following command: 
	```bash
	git clone https://github.com/not-nic/skrapbuk-christmas.git
	cd skrapbuk-christmas
	``` 
3. install the required python packages & required dependencies:
	```bash
	pip install -r requirements.txt
	npm install
	```
4. Navigate to app.py and replace `SQLALCHEMY_DATABASE_URI` with your own MySQL database URI, I chose to run mine through docker. 
	```bash
	docker run --name mysql -e MYSQL_ROOT_PASSWORD=password -d mysql:latest
	sudo nano app.py
	app.config["SQLALCHEMY_DATABASE_URI"] = "YOUR_DATABASE_URI_HERE"
	```
5. Start a flask shell session and create the database tables:
	```bash
	flask shell
	>>> from app import database
	>>> database.create_all()
	>>> exit()
	```
6. Now, start both the frontend & flask application by using:
	```bash
	flask run --debug --port 8080 --host 0.0.0.0
	npm run dev
	```
## Deployment Guide
#### Run with Docker (WIP):
1. navigate to [vite.config.ts](https://github.com/not-nic/skrapbuk-christmas/blob/master/vite.config.ts) and update proxy target:
	```bash
	sudo nano vite.config.ts
	target: "http://YOUR_DOMAIN:YOUR_BACKEND_PORT/",
	```
2. Run docker compose build. 
	```bash
	docker compose up --build
	```
	*note: this is current a WIP [(see issue)](https://github.com/not-nic/skrapbuk-christmas/issues/23) and will only deploy an Nginx container for frontend. See deploy manually step 2, for required app.py changes.* 
#### Deploy manually:
1. Build the application:
	```bash
	npm run build
	```
2. Navigate to app.py & update `DISCORD_REDIRECT_URI` & `FRONTEND_BASE_URL`
	```bash
	sudo nano app.py
	app.config["DISCORD_REDIRECT_URI"] = "http://YOUR_DOMAIN:8080/callback"
	app.config['FRONTEND_BASE_URL'] = "http://YOUR_DOMAIN"
	```
3. Copy the files from the created `dist` folder or follow [this guide](https://vitejs.dev/guide/build.html).

4. As this web app uses vue-router, you will need to make changes to either a `nginx.conf` or apache2 `.htaccess` file.
#### Apache2 
```bash
RewriteEngine On

RewriteRule ^api/(.*) http://YOUR_DOMAIN_HERE:8080/$1 [P,L]
RewriteRule ^api(/|$) http://YOUR_DOMAIN_HERE:8080/$1 [R=301,L]

<IfModule mod_negotiation.c>
  Options -MultiViews
</IfModule>

<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /skrapbuk
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```

#### Nginx

```bash
server {  
    listen 3000;  
  
    location /api/ {  
        proxy_pass http://YOUR_DOMAIN_HERE:8080/;  
        proxy_set_header Host $host;  
        proxy_set_header X-Real-IP $remote_addr;  
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;  
        proxy_set_header X-Forwarded-Proto $scheme;  
    }  
  
    location / {  
        root /usr/share/nginx/html;  
        index index.html;  
        try_files $uri $uri/ /index.html;  
    }  
}
```

