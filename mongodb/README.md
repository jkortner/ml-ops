# MongoDB Storage Container

The MongoDB installation is based on Docker. For installing Docker see [here](../README.md).


## MongoDB container

1. Setup a persistent Docker volume that  we will use to store the database (this step can be omitted as the volume is implicitly created if not present in step 2):
   ```
   docker volume create mongodb_data
   ```
2. Initialize and start the [container](https://hub.docker.com/_/mongo):
   ```
   docker run -d -p 27017-27019:27017-27019 --name mongodb --mount src=mongodb_data,dst=/data/db mongo:4.2
   ```
 3. Afterwards, the container is started and stopped by referring to its name:
    ```
    docker {start|stop} mongodb
    ```
 4. Inspect the containers log messages:
    ```
    docker logs mongodb
    ```

Notes:

 - There are two major ways to handle persistent data. Docker Toolbox on macOS only supports `volume`.
 - `-d` sends the container to the background.
 - `-p` defines a port mapping between the container and the Docker host. Otherwise, only other containers in the same Docker network (installation) can connect to the MongoDB.
 - `--name` defines the identifier for the container (convenience).
 - `--mount` defines the mapping between the Docker volumes (identified as `mongodb-vol`) and a container directory (`/data/db` is where MongoDB stores the data by default).   

 ## Test the container

 1. Setup a virtual environment and install the requirements (current working directory: `ml-ops`)
    ```
    python3 -m venv venv_mongodb
    source venv_mongodb/bin/activate
    pip install -r monogodb/requirements.txt
    ```
2. Run the sample script. The script prints the database contents and adds an entry to the database using the [pymongo](https://api.mongodb.com/python/current/tutorial.html) API. If you run the script multiple times, the number of database entries should accumulate.
    ```
    python3 mongodb/mongo_connection.py
    ```
    Note: Due to the persistent volume, your entries should not be lost after stopping and starting the container.

**Important**: The json-style entries are not intended for storing binary data. Use the Python [gridfs](https://api.mongodb.com/python/current/api/gridfs/index.html#module-gridfs) API for this purpose.

To deactivate the `venv` after testing the container run: `deactivate`.