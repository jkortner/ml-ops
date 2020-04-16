# MLOps

The aim of this project is to test tools for MLOps and provide a minimal version of a platform. 

## Overview

<p align="center">
  <img src=images/ml-ops.png>
</p>

## Docker

Most of the components used in the DevOps and MLOps pipelines are based on Docker. Here are some recommendations to install Docker on macOS:

1. Install Docker Desktop (Docker for Mac) via homebrew:
   ```
   brew cask install docker
   ```

2. Start the Docker application (installed in /Applications) in order to have the command line extensions installed (WARNING: this conflicts with Docker Toolbox)

Notes: 
 - `brew cask install docker` is different from `brew install docker docker-machine docker-compose` which installs the old Docker Toolbox that requires virtualbox. Docker Desktop comes with its own virtualization framework.
 - You do not have to create a Docker account. The command line tools will just work.
 - The operations below will most likely work with Docker Toolbox but have been tested only with Docker Desktop. 
 - According to the MongoDB Docker [documentation (Section *Where to store data*)](https://hub.docker.com/_/mongo) the virtualbox shared folder mechanism (used for direct mount binds) might be incompatible (potentially depending on the virtualbox version):
>WARNING (Windows & OS X): The default Docker setup on Windows and OS X uses a VirtualBox VM to host the Docker daemon. Unfortunately, the mechanism VirtualBox uses to share folders between the host system and the Docker container is not compatible with the memory mapped files used by MongoDB (see [vbox bug](https://www.virtualbox.org/ticket/819), [docs.mongodb.org](https://docs.mongodb.com/manual/administration/production-notes/#fsync-on-directories) and related [jira.mongodb.org](https://jira.mongodb.org/browse/SERVER-8600) bug). This means that it is not possible to run a MongoDB container with the data directory mapped to the host.
