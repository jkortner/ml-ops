# SonarQube server

Below you will find a brief description on how to use [SonarQube with Docker](https://hub.docker.com/_/sonarqube/). 
Some recommendations regarding a Docker installation on macOS can be found [here](../README.md).

Follow the step below in order to set up SonarQube in a Docker container and analyze the Python code in [sample_project](../sample_project).

## Setting up the SonarQube server

1. Run the sonarqube Docker image (latest version 8.2)
   ```
   docker run -d --name sonarqube --stop-timeout 3600 -p 9000:9000 sonarqube
   ```

   - `-d` run in background
   - `--name` identifier of the container
   - `--stop-timeout` wait for 3600 seconds until forcing container to stop (see [sonarqube container docu](https://hub.docker.com/_/sonarqube/), Section *Avoid hard termination of SonarQube*)
   - `-p` port forwarding from container to Docker host

  2. Access SonarQube at `http://localhost:9000` and login as *admin*/*admin*
  3. There is no need to manually create a project in the web interface as it can be created automatically by publishing analysis reports (see below)

## Generating reports from macOS

 1. Setup a virtual environment and install the requirements (current working directory: `ml-ops`):
    ```
    python3 -m venv venv_sampleproject
    source venv_sampleproject/bin/activate
    pip install -r sample_project/requirements.txt
    ```

 2. Configure the SonarQube project with [sample_project/sonar-project.properties](sample_project/sonar-project.properties):
    ```
    # unique project identifier
    sonar.projectKey=SampleProject
    # project display name in web interface
    #sonar.projectName=SampleProject	
    sonar.projectVersion=0.1
    # encoding
    sonar.sourceEncoding=UTF-8
    
    # source directory/package (must contain __init__.py) 
    sonar.sources=project
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

 3. Install the sonarqube client used for generating and sending reports:    
    ```
    brew install sonar-scanner
    ```
4. Generate and send report (current working directory: `ml-ops/sample_project`):
   ```bash
   ./sonar-update.sh
   ```
   The [bash script](sample_project/sonar-update.sh) generates external reports (unittests, coverage, pylint, bandit) and runs `sonar-scanner` in order to generate internal reports and transmit all reports to SonarQube server at http://localhost:9000 (default).
   Notes: 
    - [`nosetests`](https://nose.readthedocs.io/en/latest/usage.html) creates unittest results and unittest code coverage, see `nosetests -h`
    - [`pylint`](https://www.pylint.org) creates code analysis report with respect to [PEP8](https://www.python.org/dev/peps/pep-0008/) compliance.
      Messages have to follow a defined format, see [SonarQube docu](https://docs.sonarqube.org/latest/analysis/languages/python/) (section Pylint) and `pylint -h`
    - [`bandit`](https://pypi.org/project/bandit/) create code analysis reports with respect to common security issues in Python, SonarQube expects json report, also see `bandit -h`

5. Go to `http://localhost:9000`. The project has been created with default quality profiles, see *Project Settings*.
6. In the web interface, login as administrator *admin*/*admin* and create a custom Python quality profile that inherits from the default Python profile. Add all rules available (except the rules tagged as deprecated) which results in 468 active rules and 34 inactive rules (the default Python profile has 101 active rules). Note that rules are updated in the SonarQube repositories, thus, the exact numbers will change.   
7. Repeat step 4 and re-run `sonar-update.sh`. The project statistic in the web interface should have updated and report one bug for the failed unittest and 8 code smells for PEP8 violations.

To deactivate the `venv` after testing the container run: `deactivate`.

Further configurations are described in the SonarQube [documentation](https://docs.sonarqube.org/latest/).

## Generating reports from Docker

TODO

