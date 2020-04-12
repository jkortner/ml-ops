
# Sample Project

Intended for demonstrating Dev-Ops integration with:

 - Jenkins and SonarQube (**open**)
 - Docker (**open**)
 - Docker compose, e.g., interaction with MongoDB container (**open**)
 
 and ML-Ops integration with:

  - train/test data versioning (**open**)
  - prediction model versioning based on data and meta parameters (**open**)
  - third party ML workflow management tools (**open**)

The project structure follows ideas discussed on [stackoverflow](https://stackoverflow.com/questions/193161/what-is-the-best-project-structure-for-a-python-application). Most importantly:

 - Use a top-level `README.md` file (this file).
 - Use a top-level `requirements.txt` file for dependency management.
 - Don't use an `src` directory, the `sample_project` directory should be added to the `PYTHONPATH`.
 - Use a top-level `tests` directory for unit tests.


 