TESTS=tests
REPDIR=.sonarreports
NOSETESTSREP=$(REPDIR)/nosetests.xml
COVERAGEREP=$(REPDIR)/coverage.xml
PYLINTREP=$(REPDIR)/pylint_report.txt
BANDITREP=$(REPDIR)/bandit_report.json
NAME:=$(shell python setup.py --name)
VERSION:=$(shell python setup.py --version)
PACKAGE=$(NAME)
SONARHOST=localhost
SONARPORT=9000
SONARNOSCM=False
DOCKERNET=sonarqube_net

.PHONY: help clean clean-all bdist_wheel dev_deps sonar deploy

## 
## Makefile for building and testing Python package 
## including code analysis and reporting to SonarQube
## 
## Targets:
## 
## help:        Print this comment-generated help message
help:
	@sed -n 's/^## //p' Makefile

## clean:       Clean up auto-generated files 
clean:
	rm -f $(NOSETESTSREP) $(COVERAGEREP)
	rm -f $(PYLINTREP) $(BANDITREP)

## clean-all:   Clean up auto-generated files and directories 
##              (WARNING: do not store user data in auto-generated directories)
clean-all: clean
	rm -rf $(NAME).egg-info
	rm -rf build
	rm -rf dist

## bdist_wheel: Build a Python wheel with setuptools (based on setup.py)
bdist_wheel:
	python setup.py bdist_wheel

## dev_deps:    Install development dependencies (based on setup.py)
##              (installation within a Python virtual environment is recommended)
dev_deps:
	pip install -r requirements.txt

## sonar:       Report code analysis and test coverage results to SonarQube
##              (requires SonarQube server instance at http://localhost:9000, 
##               run `docker-compose up` in ./sonarqube/)
##              (requires code analysis dependencies, intall with `make dev_deps`)
##              (requires SonarQube client sonar-scanner, 
##               install with `brew sonar-scanner` or see ./Dockerfile)
sonar: $(NOSETESTSREP) $(COVERAGEREP) $(PYLINTREP) $(BANDITREP)
	sonar-scanner -Dsonar.host.url=http://$(SONARHOST):$(SONARPORT) \
              -Dsonar.projectKey=$(NAME) \
              -Dsonar.projectVersion=$(VERSION) \
              -Dsonar.sourceEncoding=UTF-8 \
              -Dsonar.sources=$(PACKAGE) \
              -Dsonar.tests=$(TESTS) \
              -Dsonar.scm.disabled=$(SONARNOSCM) \
              -Dsonar.python.xunit.reportPath=$(NOSETESTSREP) \
              -Dsonar.python.coverage.reportPaths=$(COVERAGEREP) \
              -Dsonar.python.pylint.reportPath=$(PYLINTREP) \
              -Dsonar.python.bandit.reportPaths=$(BANDITREP)

## deploy:      Build docker image for Python application including
##              code analysis and reporting to SonarQube (multi-stage build)
deploy:
	docker build --rm --network=$(DOCKERNET) -t $(NAME) .

# leading - ignores error codes, make would fail if test case fails
$(NOSETESTSREP):
	mkdir -p $(REPDIR)
	-nosetests --with-xunit --xunit-file=$@ --where $(TESTS)

# leading - ignores error codes, make would fail if test case fails
$(COVERAGEREP):
	mkdir -p $(REPDIR)
	-nosetests --with-coverage --cover-xml --cover-xml-file=../$@ --where $(TESTS)
	
# --exit-zero always return exit code 0: make would fail otherwise
$(PYLINTREP): 
	mkdir -p $(REPDIR)
	pylint $(PACKAGE) --exit-zero --reports=n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > $@

# leading - ignores error codes, make would fail if test case fails
$(BANDITREP):
	mkdir -p $(REPDIR)
	-bandit -r $(PACKAGE) --format json >$@

