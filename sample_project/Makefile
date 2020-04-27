TESTS=tests
NOSETESTSREP=$(TESTS)/nosetests.xml
COVERAGEREP=$(TESTS)/coverage.xml
PYLINTREP=pylint_report.txt
BANDITREP=bandit_report.json
NAME:=$(shell python setup.py --name)
VERSION:=$(shell python setup.py --version)
MODULE=$(NAME)

.PHONY: all clean bdist_wheel test_deps sonar

all: sonar bdist_wheel

clean:
	rm -f $(NOSETESTSREP) $(COVERAGEREP)
	rm -f $(PYLINTREP) $(BANDITREP)
	rm -rf $(NAME).egg-info
	rm -rf build
	rm -rf dist

bdist_wheel:
	python setup.py bdist_wheel

test_deps:
	pip install -r requirements.txt

# leading - ignores error codes, make would fail if test case fails
$(NOSETESTSREP):
	-nosetests --with-xunit --xunit-file=$(TESTS)/nosetests.xml --where $(TESTS)

# leading - ignores error codes, make would fail if test case fails
$(COVERAGEREP):
	-nosetests --with-coverage --cover-xml --cover-xml-file=coverage.xml --where $(TESTS)
	
# --exit-zero always return exit code 0: make would fail otherwise
$(PYLINTREP): 
	pylint $(MODULE) --exit-zero --reports=n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > $@

# leading - ignores error codes, make would fail if test case fails
$(BANDITREP):
	-bandit -r $(MODULE) --format json >$@

sonar: $(NOSETESTSREP) $(COVERAGEREP) $(PYLINTREP) $(BANDITREP)
	sonar-scanner -Dsonar.host.url=http://localhost:9000 \
              -Dsonar.projectKey=$(NAME) \
              -Dsonar.projectVersion=$(VERSION) \
              -Dsonar.sourceEncoding=UTF-8 \
              -Dsonar.sources=$(MODULE) \
              -Dsonar.exclusions=$(TESTS)/*.xml \
              -Dsonar.tests=$(TESTS) \
              -Dsonar.python.xunit.reportPath=$(NOSETESTSREP) \
              -Dsonar.python.coverage.reportPaths=$(COVERAGEREP) \
              -Dsonar.python.pylint.reportPath=$(PYLINTREP) \
              -Dsonar.python.bandit.reportPaths=$(BANDITREP)
