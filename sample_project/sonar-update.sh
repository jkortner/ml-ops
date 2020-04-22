#!/bin/bash
MODULE=project
TESTS=tests
nosetests --with-xunit --xunit-file=$TESTS/nosetests.xml --with-coverage --cover-xml-file=coverage.xml --where $TESTS
pylint $MODULE -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint_report.txt
bandit -r $MODULE --format json >bandit_report.json
sonar-scanner -Dproject.settings=sonar-project.properties 
