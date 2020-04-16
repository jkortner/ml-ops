# Jenkins build server

Below you will find a brief description on how to setup [Jenkins with Docker](https://github.com/jenkinsci/docker/blob/master/README.md). 
Some recommendations regarding a Docker installation on macOS can be found [here](../README.md).

Notes on setting up a Docker build pipeline within a Docker container:
 - Setting up a **Docker** build pipeline *within* a Docker container requires to run Docker in Docker. This could be achieved by forwarding the (Docker) host Docker daemon to the jenkins Docker container as explained in the blog post "[do-not-use-docker-in-docker-for-ci](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/)". 
 - Docker images with Docker can be found [here](https://hub.docker.com/_/docker). According to the documentation it is "generally not recommended" to run Docker in Docker.

 For the above reasons, and since we do not intend to install and manage Jenkins by ourselves, usage of the Jenkins build server will only be discussed for testing Python applications directly (outside Docker).
