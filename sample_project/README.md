
# Sample project

Intended for demonstrating DevOps/MLOps integration.

## Python project structure

The project structure follows ideas discussed on [stackoverflow](https://stackoverflow.com/questions/193161/what-is-the-best-project-structure-for-a-python-application). Most importantly for the following top-level components:

 - Use a `README.md` file (this file).
 - Use a `requirements.txt` file for setting up development environment (refers to `setup.py`).
 - Use a `setup.py` file for defining the app's pip deployment package (including dependencies). 
 - Use a `MANIFEST.in` file for advanced pip package build directives.
 - Don't use an `src` directory (redundant) but a top-level Python import package (here `sampleproject` directory).
 - Use a `tests` directory for unit tests (directory is a Python import package).
 - Use a `scripts` directory for storing scripts/binaries that are directly executable.

 The [Makefile](Makefile) file is used in order to simplify building and [code quality reporting](../sonarqube/README.md). Note that you have to setup and activate the corresponding virtual environment (see below).
```
# code quality reporting
make clean && make sonar

# building
make clean && make bdist_wheel

# or both for convenience
make clean && make
```

Documentation:
 
 - [Best practices](https://docs.python-guide.org/writing/structure/)
 - [Python packaging documentation](https://packaging.python.org/guides/distributing-packages-using-setuptools/)
 - An exemplary Python project is found on [github](https://github.com/pypa/sampleproject) 

## Python packaging with pip

Packaging your Python application with pip has the advantage that pip stores your
package contents, package dependencies and executables (along with other useful meta information)
in a single file. Applied within a virtual environment, the development and production environment is already 
quite independent of your system environment, e.g., independent of your installed system packages, preferred IDE, etc.

Setup a virtual environment for development and deployment in a production environment 
(current working directory `ml-ops`): 
```
python3 -m venv venv_sampleproject
source venv_sampleproject/bin/activate
```
Do not forget to disable to switch back to your system environment by running the `deactivate` command after you are done.

### Setup development environment

An important advantage of packaging your app with `setup.py` (pip) in contrast to specifying your app's dependencies
in the `requirements.txt` file only, is that pip will automatically link your application
sources in the `PYTHONPATH`. 
Since your dependencies will automatically be installed in the 
`PYTHONPATH`, you do not have to manually manage the `PYTHONPATH` anymore.
```
cd sample_project
pip install -r requirements.txt
```
It is **important** to change to the `sample_project` directory, because the
`requirements.txt` file refers to the `setup.py` file which is expected to be 
found in the current working directory.

[requirements.txt](requirements.txt):
```
-e .[dev]
```
Notes:

 - `-e`: Editable mode only *links* the sources to the `PYTHONPATH` and does not
 copy the sources to the `PYTHONPATH` (you can make changes to your code without 
 having to re-install your app/package).
 - `.`: The dot refers to the current working directory where the `setup.py` file is expected.
 - `[dev]`: Refers to the `dev` variant/environment of the package which is defined in `setup.py` (see `extras_require`).  

The full discussion on how to use `setup.py` together with `requirements.txt` 
is found on [stackoverflow](https://stackoverflow.com/questions/14399534/reference-requirements-txt-for-the-install-requires-kwarg-in-setuptools-setup-py/19081268#19081268)

### Build pip package for deployment 

The result of building a package from your Python application is a single wheel file (`.whl`) which can
easily be installed in any (virtual) Python environment. The package contents and its behavior are defined in
the [`setup.py`](setup.py) file. 

1. After switching to your virtual Python environment build the (binary) wheel (current working directory `ml-ops/sample_project`):
   ```
   python setup.py bdist_wheel
   # alternatively run the command with make (see Makefile):
   make bdist_wheel
   ```
   Notes (on `setup.py`):
    - `name`: The name of the pip/Python package must match the name of the top-level import package in order to let the [Makefile](Makefile) work correctly.
    - `version`: Either define your project version here or generate it accordingly. The version has to follow a defined [pattern](https://packaging.python.org/guides/distributing-packages-using-setuptools/#choosing-a-versioning-scheme).  
    - `packages`: Defines how to include/exclude Python import packages. Can be specified manually or with [find_packages](https://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages). Projects using an `src` directory ([bad practice](https://docs.python-guide.org/writing/structure/#the-actual-module)) can *include* the `src` directory only. Otherwise, you have to *exclude* everything you do not want to ship with your deployment package. 
    - `tests` directory contains unit test which are typically not part of the deployment package. Excluding tests requires `exclude` [definitions](https://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages) and [directives](https://stackoverflow.com/questions/8556996/setuptools-troubles-excluding-packages-including-data-files/11669299#11669299) in the `MANIFEST.in` file.
    - `scripts`: Provides executables which are important to easily access the functionalities provided by the package (important for use with Docker). Executables are automatically installed on the `PATH`.
    - `entry_points`: Automatically generate executables by Python package.module:function (less control than writing script yourself, e.g., for configurations). 
    - `setup_requires`: Python package dependencies required before running setup.
    - `install_requires`: Python package dependencies (corresponds to definitions in `requirements.txt`, `requirements.txt` refers to `setup.py` in order to avoid [redundancies](https://stackoverflow.com/questions/14399534/reference-requirements-txt-for-the-install-requires-kwarg-in-setuptools-setup-py/19081268#19081268)).
    - `extras_require`: Defines different environments with different dependencies, e.g., for development/testing and production. Specific environments can be installed by appending `[<env>]` to the installation target (where `<env>` is replaced by the environment key, here `dev`), see [setuptools documentation](https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-dependencies).
    - `package_data`: Non-python files that should be included in the package have to be declared specifically. Further inclusion patterns can be defined in `MANIFEST.in`.

2. Install the wheel in a test environment (`deactivate` any active virtual environment, current working directory `ml-ops`):
   ```
   # Switch back to your system environment
   deactivate

   # Create a test environment and activate it
   python3 -m venv venv_test
   source venv_test/bin/activate
   
   # Install package into fresh environment
   pip install sample_project/dist/sampleproject-0.1-py3-none-any.whl
   ``` 

3. Test the installed application:
   ```
   sampleproject --help
   ```

Documentation:
 - [Setuptools documentation](https://setuptools.readthedocs.io/en/latest/setuptools.html)
 - [Python packaging guide](https://packaging.python.org/guides/distributing-packages-using-setuptools/#setup-args) 
 - Blog post for building a [bdist_wheel](https://dzone.com/articles/executable-package-pip-install)
 - Commented [setup.py](https://github.com/pypa/sampleproject/blob/master/setup.py) (reference)
 - [Stackoverflow](https://stackoverflow.com/questions/1471994/what-is-setup-py) on what is `setup.py`

 ## Build Docker image for deployment

The [Dockerfile](Dockerfile) implements a multi-stage Docker image build for 
running unit tests, code coverage, code analysis, SonarQube reporting,
building a Python wheel in a first stage as well as installing the wheel in a
minimal image within the second stage. The Dockerfile implements the steps which
are explained [above](#build-pip-package-for-deployment).

1. For reporting analyses to SonarQube, the `sonarqube` [container](../sonarqube/README.md) must be running and must be connected to the same Docker network, which will be used in the Docker image build below:
   ```bash
   docker network create cicd
   docker network connect cicd sonarqube
   ```
2. The build process for sample_project will be triggered within the `cicd` network:
   ```bash
   docker build --rm --network=cicd -t pyapp .
   ```
   Notes:
    - `--rm` flag removes intermediate containers (also useful with `docker run`)
    - `--network` specifies the name of the Docker network for building the image
    - `-t pyapp` specifies the name of the tag that can be used to refer to the image
    - `.` refers to the current directory where Docker expects a `Dockerfile`
    - This example assumes that the current directory is (typically) the root of your git repository and, therefore, ignores the .git directory (see [.dockerignore](.dockerignore)). The repository itself should not be copied to the image for building. Consequently, the SonarQube version control support is disabled when reporting results, see flag used in [Dockerfile](Dockerfile) when calling `make`.

3. Run the newly built image by (implicitly) creating a container:
   ```bash
   docker run --rm pyapp
   ```
   Notes:
    - `--rm` deletes the container after the program terminates
    - `pyapp` specifies the name of the image
    - The container runs the script specified at `ENTRYPOINT` at the end of [Dockerfile](Dockerfile). The default argument is defined at `CMD` and can
    be overwritten the arguments to the `docker run` command above, e.g., `docker run --rm pyapp 45 46` 

4. In order to obtain the wheel that was built in the build process, copy the `dist` directory from the container to a local directory, here `dist_pyapp_container`:
   ```bash
   # Create a container
   docker container create --name pyapp pyapp
   # Recursively copy from container to Docker host
   docker cp pyapp:/dist dist_pyapp_container
   # Remove container that was created above
   docker container rm pyapp
   ```
   Notes:
    - `docker cp` does not support wildcards. Since the name of the `whl` file is generated automatically, it is easier to copy a directory with the wheel file than copying the wheel file directly (provided that the directory has a generic name).

  Also have a look at the [Dockerfile](Dockerfile) which contains detailed comments for every step.
