"""Use the quickstart example in order to test your MlFlow container:
https://mlflow.org/docs/latest/quickstart.html#using-the-tracking-api

Here, the example is extended by logging to an MlFlow tracking server
(instead of the local directory),
by storing artifacts to the (S3 compatible) MinIO object storage
and by using a single mlflow run with a given experiment name.
"""
import os
from random import random, randint
import botocore
import boto3
import mlflow


def create_bucket(bucket_name):
    s3cli = boto3.client('s3',
                         endpoint_url=os.environ.get('MLFLOW_S3_ENDPOINT_URL'))
    try:
        s3cli.create_bucket(Bucket=bucket_name)
        print(f'S3 bucket {bucket_name} has been created')
    except botocore.exceptions.ClientError as error:
        if (error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou' or
                error.response['Error']['Code'] == 'BucketAlreadyExists'):
            print('Info: bucket already exists')
        else:
            raise error


def main():
    # S3 storage configurations are provided as environment variables which
    # is a requirement of the AWS boto3 library used in the mlflow client
    # S3 storage credentials as defined for the MinIO server
    os.environ['AWS_ACCESS_KEY_ID'] = 'minio'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'minio_secret'
    # MinIO server URL (S3 compatible)
    # (adjust host:port if run within Docker network)
    os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://localhost:9001'
    # Create S3 bucket if it does not exist already
    # Name of the bucket as defined for the MlFlow server (ARTIFACT_ROOT)
    # e.g., s3://mlflow/
    bucket_name = 'mlflow'
    create_bucket(bucket_name)
    # MlFlow tracking server URL
    # (adjust host:port if run within Docker network)
    mlflow.set_tracking_uri('http://localhost:5000')
    # Create new experiment
    mlflow_exp_id = mlflow.set_experiment(experiment_name='random-test')
    # Start logging experiment data in new run for the given experiment
    with mlflow.start_run(experiment_id=mlflow_exp_id):
        # Log a parameter (key-value pair)
        mlflow.log_param("param1", randint(0, 100))

        # Log a metric; metrics can be updated throughout the run
        mlflow.log_metric("foo", random())
        mlflow.log_metric("foo", random() + 1)
        mlflow.log_metric("foo", random() + 2)

        # Log an artifact (output file)
        if not os.path.exists("outputs"):
            os.makedirs("outputs")
        with open("outputs/test.txt", "w") as f:
            f.write("hello world!")
        print(mlflow.get_artifact_uri())
        mlflow.log_artifacts("outputs")


if __name__ == "__main__":
    main()
