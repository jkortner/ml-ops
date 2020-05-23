# DVC

Data Version Control ([DVC](https://dvc.org)) is an open-source version control system for machine learning projects. Its focus is on handling large data files and it uses Git. This [blog post](https://stdiff.net/MB2019051301.html) describes the idea behind DVC: you need algorithms, hyperparameters and data to replicate a model. When managing data, the files might be to large for a Git repository. DVC creates a corresponding file for each data file and only manages the created files with Git.

In order to test DVC we set up the self-hosted Git service Gogs that runs in a Docker container, and a Python environment with an IDE in another container.

## Gogs

[Gogs](https://gogs.io) is a self-hosted Git service. A good tutorial on how to set up Gogs in a Docker container is [here](http://dbg.io/local-github-like-source-control-with-gogs-and-docker/).

```
docker pull gogs/gogs
docker run --name=gogs -p 3000:3000 -v "$(pwd)/gogs:/data" gogs/gogs
```

Your local Git service now runs on http://localhost:3000. Use the input mask to set up Gogs (here with SQLite3), create a user (here `ybml`) and a repository (`ml-ops-dvc`). If you want to stop the docker container type `docker stop gogs`. To re-start the container use `docker start gogs`. 

Note: To open a shell in a container run

```
docker exec -it gogs /bin/sh
```

## Python, Theia and Gogs

Now let's start a new container `ml-ops-gogs`, as described above, and a second connected container `ml-ops-theia` with a Python environment and the IDE Theia.

```
docker network create --driver bridge ml-ops-net
docker run -d --name=ml-ops-gogs -p 3000:3000 -v "$(pwd)/gogs:/data" --network ml-ops-net gogs/gogs
docker run -it --init --name=ml-ops-theia -p 2000:3000 -v "$(pwd):/home/project" --network ml-ops-net theiaide/theia-python:latest
```

The IDE can be reached at http://localhost:2000.

To clone the `ml-ops-dvc` repository into the second Docker container run

```
git clone http://ml-ops-gogs:3000/ybml/ml-ops-dvc.git
```

To test if everything works try to create a README and push it to the repository.

```
touch README.md
git add README.md
git commit -m "Add README"
git push
```

## DVC

Install DVC with `pip`. 

```
dvc init
```


