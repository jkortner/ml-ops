FROM python:3.8-slim-buster

# The script wait-for-it waits until a network service is available
RUN apt-get update \
    && apt-get install -y --no-install-recommends wait-for-it \
    && rm -rf /var/lib/apt/lists/*

# psycopg2 is a Python wrapper for connecting to a PostgreSQL database
# the non-binary version must be compiled, which does not seem necessary here
RUN pip install psycopg2-binary
# Install the latest version of mlflow in the system Python environment
RUN pip install mlflow 

# Create a directory for storing artifacts
RUN mkdir /mlflow

# Start the mlflow tracking server and listen for incoming connections on port
# 5000 (default, not specified in the command)
CMD wait-for-it $DB_CONN -- mlflow server \
    --backend-store-uri postgresql://$DB_AUTH@$DB_CONN/mlflow \
    --default-artifact-root /mlflow \
    --host 0.0.0.0