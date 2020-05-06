# SonarQube server

Below you will find a brief description on how to use [SonarQube with Docker](https://hub.docker.com/_/sonarqube/). 
Some recommendations regarding a Docker installation on macOS can be found [here](../README.md).

Follow the step below in order to set up SonarQube in a Docker container and analyze the Python code in [sample_project](../sample_project).

## Setting up SonarQube server with embedded database

1. Run the SonarQube Docker image (latest version 8.3):
   ```bash
   docker run -d --name sonarqube --stop-timeout 3600 -p 9000:9000 sonarqube
   ```
   Notes:
    - `-d` run in background
    - `--name` identifier of the container
    - `--stop-timeout` wait for 3600 seconds until forcing container to stop (see [SonarQube container docu](https://hub.docker.com/_/sonarqube/), section *Avoid hard termination of SonarQube*)
    - `-p` port forwarding from container to Docker host

  2. Access SonarQube at `http://localhost:9000` and login as *admin*/*admin*
  3. Note the warning at the bottom of the page informing you that you are using an embedded database which is not suitable for production (only evaluation).
  4. There is no need to manually create a project in the web interface as it can be created automatically by publishing analysis reports (see below).
  5. Stop the container with
     ```bash
     docker stop sonarqube
     ```

## Setting up SonarQube server with PostgreSQL

1. Multiple docker containers can be run with `docker-compose` (current working directory: `ml-ops/sonarqube`):
   ```bash
   docker-compose up -d
   ```
   Notes:
    - `-d` run in background
    - [docker-compose.yml (see comments)](docker-compose.yml) defines services, networks and volumes
    - `docker-compose` auto-generates names for containers (based on services), networks and volumes by prefixing each name from the [docker-compose.yml](docker-compose.yml) with `projectname_` where `projectname` defaults to the name of the current directory. The project name can be specified with command-line parameter `-p`, e.g., `docker-compose -p project up -d` or with environment variable `COMPOSE_PROJECT_NAME`, [see docker reference](https://docs.docker.com/compose/reference/envvars/#compose_project_name).     
    - Since we are only interested in preserving analysis data for projects, it is sufficient to use a single docker volume for postgresql data (`db_data`). The contents of all other directories, which might be worth preserving according to the [SonarQube documentation on Docker Hub](https://hub.docker.com/_/sonarqube/), are not modified.
    - **Attention:** database credentials are specified over the command-line. This is insecure. For example, the credentials will be visible to any user by calling `top`, try `docker-compose top`.
  2. Access SonarQube at `http://localhost:9000` and login as *admin*/*admin*
  3. Note that the embedded database warning at the bottom of the page (see above) disappeared.
  4. There is no need to manually create a project in the web interface as it can be created automatically by publishing analysis reports (see below).
  5. Stop and remove the containers with
     ```bash
     docker-compose -p sonarqube stop
     ```


## Generating reports from macOS

 1. Setup a virtual environment and install the requirements (current working directory: `ml-ops`):
    ```bash
    python3 -m venv venv_sampleproject
    source venv_sampleproject/bin/activate
    pip install -r sample_project/requirements.txt
    ```

 2. Install the SonarQube client used for generating and sending reports:    
    ```bash
    brew install sonar-scanner
    ```

 4. Configure the SonarQube project with `sonar-scanner` command-line arguments in the `sample_project` [Makefile](../sample_project/Makefile):

3. Generate and send report (current working directory: `ml-ops/sample_project`):
   ```bash
   make clean && make sonar
   ```
   The [Makefile](../sample_project/Makefile) has targets for generating external reports (unittests, coverage, pylint, bandit) and running `sonar-scanner` in order to generate internal reports and transmit all reports to SonarQube server at http://localhost:9000 (default).
   Notes: 
    - [`nosetests`](https://nose.readthedocs.io/en/latest/usage.html) creates unittest results and unittest code coverage, see `nosetests -h`
    - [`pylint`](https://www.pylint.org) creates code analysis report with respect to [PEP8](https://www.python.org/dev/peps/pep-0008/) compliance.
      Messages have to follow a defined format, see [SonarQube docu](https://docs.sonarqube.org/latest/analysis/languages/python/) (section Pylint) and `pylint -h`
    - [`bandit`](https://pypi.org/project/bandit/) create code analysis reports with respect to common security issues in Python, SonarQube expects json report, also see `bandit -h`
    - [sonar-scanner](https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/) is configured with command line flags according to:
      ```
      # SonarQube URL
      sonar.host.url=http://localhost:9000
      # unique project identifier
      sonar.projectKey=sampleproject
      # project display name in web interface
      #sonar.projectName=sampleproject	
      sonar.projectVersion=0.1
      # encoding
      sonar.sourceEncoding=UTF-8
    
      # source directory/package (must contain __init__.py) 
      sonar.sources=sampleproject
      # exclude generated unittest reports from analysis
      sonar.exclusions=tests/*.xml
    
      # unittests directory/package (must contain __init__.py)
      sonar.tests=tests
      # report for unittest results
      sonar.python.xunit.reportPath=tests/nosetests.xml
      # report for unittest coverage
      sonar.python.coverage.reportPaths=tests/coverage.xml
      # linting
      sonar.python.pylint.reportPath=pylint_report.txt
      sonar.python.bandit.reportPaths=bandit_report.json
       ```
    
      The full documentation can be found [here](https://docs.sonarqube.org/latest/analysis/analysis-parameters/) and Python related settings can be found [here](https://docs.sonarqube.org/latest/analysis/coverage/).

4. Go to `http://localhost:9000`. The project has been created with default quality profiles, see *Project Settings*.
5. In the web interface, login as administrator *admin*/*admin* and create a custom Python quality profile that inherits from the default Python profile. Add all rules available (except the rules tagged as deprecated) which results in 468 active rules and 34 inactive rules (the default Python profile has 101 active rules). Note that rules are updated in the SonarQube repositories, thus, the exact numbers will change.   
6. Repeat step 4 and re-run `make sonar`. The project statistic in the web interface should have updated and report one bug for the failed unittest and 8 code smells for PEP8 violations.

You might want to have a look at the *Quality Gates* in the web interface that define conditions for determining whether your code meets the minimum quality standards. Note that SonarQube follows the [*clean as you code*](https://docs.sonarqube.org/latest/user-guide/clean-as-you-code/) principle, thus, quality gates are only applied on new code by default (there are settings for *overall code*). 

Further configurations are described in the SonarQube [documentation](https://docs.sonarqube.org/latest/).

To deactivate the `venv` after testing the container run: `deactivate`.


## Generating reports from Docker

Docker images are supposed to be minimal, thus, installing test tools and `sonar-scanner` is not a good idea for images intended for deployment. [Multi-stage builds](https://docs.docker.com/develop/develop-images/multistage-build/) allow for building and testing in an intermediate image, before installing the final application into a minimal deployment image.

The [sample_project](../sample_project/README.md) demonstrates the following approach:
1. Define a Python pip package including dependencies and application code with [setup.py](../sample_project/setup.py).
2. Define [Makefile](../sample_project/Makefile) targets `dev_deps` and `sonar` in oder to easily install (development) dependencies and run `sonar-scanner`.
3. Define a multi-stage [Dockerfile](../sample_project/Dockerfile).

   First stage (based on a Python based image):
    - Installs `sonar-scanner` 
    - Install the application dependencies 
    - Run `sonar-scanner` and build a Python wheel (`make all`, `all` is the default target and does not have to be specified)

   Second stage (based on a Python base image):
    - Copy the wheel Python package to the final deployment image
    - Install the wheel Python package

