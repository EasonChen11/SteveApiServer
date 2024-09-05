1. copy .env.backend to .env and copy .flaskenv.backend to .flaskenv
2. modify .env and .flaskenv

   > FLASK_APP= your flask app file
   > 
   > API_KEY= your steVe API key
   >
   > DOCKER_NETWORK=
   >
   >> docker network ls
   >> 
   >> docker network inspect <network>
   >>
   >> find your steve network

   > DOCKER_PORT= your steVe port

3. run code

```yaml
docker-compose up --build
```
