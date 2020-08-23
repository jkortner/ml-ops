FROM python:3.8-slim-buster

# Default arguments
ARG DB_AUTH=mlflow:mlflow
ARG DB_CONN=db:5432
ARG ARTIFACT_ROOT=s3://mlflow/
ARG MLFLOW_S3_ENDPOINT_URL=http://minio:9000
ARG AWS_ACCESS_KEY_ID=minio
ARG AWS_SECRET_ACCESS_KEY=minio_secret
# Generate environment variables from arguments
ENV DB_AUTH=${DB_AUTH}
ENV DB_CONN=${DB_CONN}
ENV ARTIFACT_ROOT=${ARTIFACT_ROOT}
ENV MLFLOW_S3_ENDPOINT_URL=${MLFLOW_S3_ENDPOINT_URL}
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

# The script wait-for-it waits until a network service is available
RUN apt-get update \
    && apt-get install -y --no-install-recommends wait-for-it \
    && rm -rf /var/lib/apt/lists/*

# psycopg2 is a Python wrapper for connecting to a PostgreSQL database
# the non-binary version must be compiled, which does not seem necessary here
#
# boto3 provides the AWS S3 client API
# The AWS client (and credentials) are required for reading artifacts in the
# MlFlow web interface. The (Python) script that logs the artifacts, access the
# S3 storage directly and does, therefore, need its own client/credentials.
#
# Install the latest version of mlflow in the system Python environment
RUN pip install psycopg2-binary boto3 mlflow 

# Start the mlflow tracking server and listen for incoming connections on port
# 5000 (default, not specified in the command)
CMD wait-for-it $DB_CONN -- mlflow server \
    --backend-store-uri postgresql://$DB_AUTH@$DB_CONN/mlflow \
    --default-artifact-root $ARTIFACT_ROOT \
    --host 0.0.0.0