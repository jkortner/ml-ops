# MLFlow Tracking Server

The MLFlow server allows you to keep track of your machine learning experiments
and provides APIs for various languages. In the following, an MLFlow server will
be started in a dockerized environment through [`docker-compose.yml`](docker-compose.yml).

Assuming the project name/context of the docker compose file is `mlflow`:

- If not present, builds an `mlflow` Docker image with [`Dockerfile`](Dockerfile).
- MLFlow artifacts will be stored in the Docker volume `mlfow_artifacts`.
- Starts a PostgreSQL server for storing experiment data. The database is stored
  in the Docker volume `mlflow_db_data`.
- MLFlow server and the PostgreSQL server will run in the same Docker network
  `mlflow_net`.
- The MLFlow server can be reached at [http://localhost:5000](http://localhost:5000).
- In order to inspect the database directly, uncomment the `adminer`
  service in `docker-compose.yml` and access the server at [http://localhost:8055](http://localhost:8055).

Start the services (working directory `ml-ops/mlflow`):

```bash
docker-compose up -d
# Shutdown (might take a moment)
docker-compose down
```
