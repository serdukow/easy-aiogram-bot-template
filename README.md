
Easy Aiogram Bot
==============
![Python](https://img.shields.io/badge/python-3.12.3-blue)
![Aiogram](https://img.shields.io/badge/Aiogram-^3.17.0-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-^0.115.6-green)

Easily make scalable Aiogram bots with this template. This template is designed to help you quickly build, configure, and deploy Aiogram-based bots with a flexible and scalable structure.
![](https://i.imgur.com/waxVImv.png)

Features
==============


- **Poetry**: Use [Poetry](https://python-poetry.org/) for managing dependencies and virtual environments.
- **Webhook Support**: Easily configure and deploy bots with webhooks for scalability.
- **Nginx Integration**: Easily integrate Nginx for serving your bot over HTTPS and managing webhooks.
- **Logging & Monitoring**: Simple logging configuration for better debugging and monitoring.
- **Dockerized**: Fully Dockerized, making it easy to deploy your bot in any environment.
- **Postgres**: Seamlessly integrate PostgreSQL for reliable and scalable database storage.
- **Redis**: Fully Dockerized, so it can be easily deployed alongside your bot in any environment. The Redis setup supports scaling, making it suitable for high-traffic bots.
----------------------

Usage
==============

To quickly get started with the bot, follow the steps below.

Prerequisites
==============

### Clone repository

```bash
git clone https://github.com/serdukow/easy-aiogram-bot.git
cd easy-aiogram-bot
```
### Webhook prerequisites
If you want **to use webhook**, ensure you have your own domain.  
Then proceed to [How to Set Webhook](#how-to-set-webhook). 
### Polling prerequisites
To start bot without webhook, just fill `.env` with your keys, then verify it by run this command in terminal:
```
poetry run pytest tests/test_polling.py
```
then **remove services nginx, certbot** from `docker-compose.yml` and finally:
```
docker compose up --build
```
----------------------
How to set Webhook
==============

To set up the webhook, follow these steps:

1. **Set your domain** in the `.env` file under the `NGINX_HOST` variable.
```
NGINX_HOST=your-domain.com
```
2. **Build and start** the Docker containers using the .env file:
```bash
docker compose --env-file .env build
docker compose run --rm -d -p 80:80 nginx
```

3. **Verify the setup**
Check if your Nginx server is up and running by using curl:
```
curl http://your-domain.com
```
If you receive an HTTP 301 redirect, everything is working fine.

4. **Simulate certificate issuance:**

```
docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d your-domain.com
```
If the dry run is successful, you should see a message saying: **The dry run was successful.**

5. **Issue the SSL certificate:**

```
docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d your-domain.com
```

6. **Stop the containers:**

```
docker compose kill && docker compose down
```

7. **Update docker-compose.yml:**

Make sure your docker-compose.yml file is correctly configured for Nginx templates:

```
volumes:
# - ./nginx/initial:/etc/nginx/templates/:ro
- ./nginx/templates:/etc/nginx/templates/:ro
  ```

8. **Finally** verify  and restart with the final setup, do not forget to set this vars in `.env`:
```
USE_WEBHOOK=True
``` 
```
WEBHOOK_URL='https://your-domain.com'
```
then run test:
```
poetry run pytest tests/test_webhook.py
```
finally compose
```
docker compose up --build
```

**Renewing SSL Certificate:**
After 3 months, you’ll need to renew the SSL certificate. To do so, run:
```
docker compose up
dockercompose run --rm certbot renew
```
----------------------
Roadmap
==============

- [x] Tests
  - [x] Basic
  - [ ] Versions
- [ ] Webapp Integration
- [ ] React frontend for webapp
----------------------
Contributing
==============
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.
----------------------
Special thanks
==============
[@ssharkexe](https://github.com/ssharkexe)




