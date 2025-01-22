
Easy Aiogram Bot Template
==============
![Python](https://img.shields.io/badge/python-3.12.3-yellow)
![Aiogram](https://img.shields.io/badge/Aiogram-3.17.0-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-red)

🤖 Simple, but powerful template for scalable Aiogram bots.
![](https://i.imgur.com/waxVImv.png)

Features
==============

- **Poetry**: As main dependency and package manager.


- **Webhook Support**: Easily configure and deploy bots with webhooks.


- **Nginx Integration**: Serving your bot over HTTPS and manage webhooks.


- **Logging & Monitoring**: Logging, debugging and monitoring.


- **Dockerized**: Fully Dockerized.


- **Postgres**: As main database storage.


- **Alembic**: Migration tool.


- **Redis**: As main cache storage


- **Localization**: Translatable support for different languages with.
----------------------

Get started
==============

### Clone repository

```bash
git clone https://github.com/serdukow/easy-aiogram-bot-template.git
cd easy-aiogram-bot-template
```
### Webhook
<details>
  <summary>Click for Webhook installation details</summary>

Ensure you have your **own domain** and **any VPS**. 


To set up the webhook, **follow these steps**:

1. **Set your domain** in the `.env` file under the `NGINX_HOST` variable.
```
NGINX_HOST=your-domain.com
```
2. **Build and start** the Docker containers using the .env file:
```bash
docker compose --env-file .env build
docker compose run --rm -d -p 80:80 nginx
```

3. **Verify it** by using curl:
```
curl http://your-domain.com
```
If you receive an HTTP 301 redirect, everything is working fine.

4. **Simulate certificate issuance:**

```
docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d your-domain.com
```
If the dry run is successful, you should see a appropriate message

5. **Issue the SSL certificate:**

```
docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ -d your-domain.com
```

6. **Stop the containers:**

```
docker compose kill && docker compose down
```

7. **Update docker-compose.yml for production:**

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
WEBHOOK_HOST='https://your-domain.com'
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

</details>

### Polling
<details>
  <summary>Click for Polling installation details</summary>
To start bot without webhook, just fill `.env` with your keys, then verify it by run this command in terminal:
```
poetry run pytest tests/test_polling.py
```
then **remove services nginx, certbot** from `docker-compose.yml` and finally:
```
docker compose up --build
```
</details>

----------------------
Roadmap
==============

- [x] Tests
  - [x] Basic
  - [ ] Versions
- [ ] React Webapp integration
- [x] Database
  - [x] Alembic 
----------------------
Contributing
==============

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

# Special thanks
[@ssharkexe](https://github.com/ssharkexe)




