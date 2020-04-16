# MongoDB Storage Container

## Docker Installation

1. Install Docker Desktop (Docker for Mac) via homebrew:
   ```
   brew cask install docker
   ```

2. Start the Docker application (installed in /Applications) in order to have the command line extensions installed (WARNING: this conflicts with Docker Toolbox)

Notes: 
 - `brew cask install docker` is different from `brew install docker docker-machine docker-compose` which installs the old Docker Toolbox that requires virtualbox. Docker Desktop comes with its own virtualization framework.
 - You do not have to create a Docker account. The command line tools will just work.
 - The operations below will most likely work with Docker Toolbox but have been tested only with Docker Desktop. 

## MongoDB Container

1. Setup a persistent Docker volume that  we will use to store the database (this step can be omitted as the volume is implictely created if not present in step 2):
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