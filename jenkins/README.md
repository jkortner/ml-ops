# Jenkins build server

Below you will find a brief description on how to setup [Jenkins with Docker](https://github.com/jenkinsci/docker/blob/master/README.md). 
Some recommendations regarding a Docker installation on macOS can be found [here](../README.md).

Notes on setting up a Docker build pipeline within a Docker container:
 - Setting up a **Docker** build pipeline *within* a Docker container requires to run Docker in Docker. This could be achieved by forwarding the (Docker) host Docker daemon to the jenkins Docker container as explained in the blog post "[do-not-use-docker-in-docker-for-ci](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/)". 
 - Docker images with Docker can be found [here](https://hub.docker.com/_/docker). According to the documentation it is "generally not recommended" to run Docker in Docker.
 - [how-to-build-docker-images-inside-a-jenkins-container](https://medium.com/@manav503/how-to-build-docker-images-inside-a-jenkins-container-d59944102f30) describes the steps required for running Docker in Docker.

 For the above reasons, and since we do not intend to install and manage Jenkins by ourselves, Jenkins is not suitable for a Docker-based DevOps / MLOps pipeline.
 However, here are some notes on how to get started with the jenkins Docker container:

1. Run the [jenkins:lts Docker container](https://github.com/jenkinsci/docker/blob/master/README.md):
   ```
   docker run -d --name jenkins -v jenkins_home:/var/jenkins_home -v <git_repo>:/var/jenkins_repo -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
   ```

   - `-d` run in background
   - `--name` identifier of the container
   - `-v jenkins_home:...` implicitly create otherwise use jenkins_home Docker volume for persistent data
   - `-v <git_repo>`:/var/jenkins_repo` bind mount local git repository path to `/var/jenkins_repo` in container
   - `-p` port forwarding from container to Docker host

2. Access jenkins at `http://localhost:8080` and obtain access token from container log:
   ```
   docker logs jenkins
   ```
3. Create user and install recommended plugins
4. Add *Freestyle project* and add local git repository (see above) with url:
   ```
   file:///var/jenkins_repo
   ```
5. Run build which should already show you the hash and comment of the last git commit in the *Console Output*
6. Set up a Python build pipeline which will typically involve running unit tests and/or code metrics as Python does not need to be "build". A Python environment is required for this purpose:

   - Some general information including links can be found at [jenkins.io/solutions/python](https://jenkins.io/solutions/python/)
   - The environment might by provided by Jenkins plugins, like [ShiningPanda](https://plugins.jenkins.io/shiningpanda/). (Only Python2.7 has been available out of the box)
   - You could extend the Jenkins Docker image by installing the Python environment by yourself. See this [blog article](http://www.alexconrad.org/2011/10/jenkins-and-python.html) for setting up Jenkins and Python on a Ubuntu machine. 
