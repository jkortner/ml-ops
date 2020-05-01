TESTS=tests
REPDIR=.sonarreports
NOSETESTSREP=$(REPDIR)/nosetests.xml
COVERAGEREP=$(REPDIR)/coverage.xml
PYLINTREP=$(REPDIR)/pylint_report.txt
BANDITREP=$(REPDIR)/bandit_report.json
NAME:=$(shell python setup.py --name)
VERSION:=$(shell python setup.py --version)
MODULE=$(NAME)
SONARHOST=localhost
SONARPORT=9000
SONARNOSCM=False

.PHONY: all clean bdist_wheel dev_deps sonar

all: sonar bdist_wheel

clean:
	rm -f $(NOSETESTSREP) $(COVERAGEREP)
	rm -f $(PYLINTREP) $(BANDITREP)
	rm -rf $(NAME).egg-info
	rm -rf build
	rm -rf dist

bdist_wheel:
	python setup.py bdist_wheel

dev_deps:
	pip install -r requirements.txt

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
	pylint $(MODULE) --exit-zero --reports=n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > $@

# leading - ignores error codes, make would fail if test case fails
$(BANDITREP):
	mkdir -p $(REPDIR)
	-bandit -r $(MODULE) --format json >$@

sonar: $(NOSETESTSREP) $(COVERAGEREP) $(PYLINTREP) $(BANDITREP)
	sonar-scanner -Dsonar.host.url=http://$(SONARHOST):$(SONARPORT) \
              -Dsonar.projectKey=$(NAME) \
              -Dsonar.projectVersion=$(VERSION) \
              -Dsonar.sourceEncoding=UTF-8 \
              -Dsonar.sources=$(MODULE) \
              -Dsonar.tests=$(TESTS) \
              -Dsonar.scm.disabled=$(SONARNOSCM) \
              -Dsonar.python.xunit.reportPath=$(NOSETESTSREP) \
              -Dsonar.python.coverage.reportPaths=$(COVERAGEREP) \
              -Dsonar.python.pylint.reportPath=$(PYLINTREP) \
              -Dsonar.python.bandit.reportPaths=$(BANDITREP)
