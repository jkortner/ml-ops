# MLFlow Tracking Server

The [MLFlow](https://mlflow.org) server allows you to keep track of your machine learning experiments
and provides APIs for various languages. In the following, an MLFlow server will
be started in a dockerized environment through [`docker-compose.yml`](docker-compose.yml).

Assuming the project name/context of the docker compose file is `mlflow`:

- If not present, builds an `mlflow` Docker image with [`Dockerfile`](Dockerfile).
- MLFlow artifacts will be stored in the Docker volume `mlfow_artifacts`.
- Starts a PostgreSQL server for storing experiment data. The database is stored
  in the Docker volume `mlflow_db_data`.
- Starts a MinIO server for storing artifacts. The buckets are stored
  in the Docker volume `mlflow_minio_data`.
- MLFlow server, PostgreSQL server and the MinIO server will run in the same Docker network `mlflow_net`.
- The MLFlow server can be reached at [http://localhost:5000](http://localhost:5000).
- The MinIO server can be reached at [http://localhost:9001](http://localhost:9001).
- In order to inspect the PostgreSQL database directly, uncomment the `adminer`
  service in `docker-compose.yml` and access the server at [http://localhost:8055](http://localhost:8055).

Start the services (working directory `mlflow`):

```bash
docker-compose up -d
# Shutdown (might take a moment)
docker-compose down
```

## Test the container

1. Setup a virtual environment and install the requirements (working directory: `mlflow`)

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install mlflow boto3
   ```

   Note: `boto3` contains the AWS client library for accessing the (S3 compatible) MinIO server.

2. Run the sample script. The script creates the S3-compatible bucket `mlflow` in the MinIO server. It creates an experiment and log sample parameters, metrics and an artifact (e.g., a model file) to the MlFlow tracking server. Note that the artifacts are written to the S3 storage directly. Therefore, the client needs access information/credentials for the S3 storage.

   ```bash
   python3 mlflow_sample.py
   ```

3. Go to [http://localhost:5000](http://localhost:5000) and you should see the logged experiment data including the artifact within the `random-test` experiment.
4. Go to [http://localhost:9001](http://localhost:9001) and you should see the artifact within the `mlflow` bucket.
