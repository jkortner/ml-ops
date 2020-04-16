# Sandbox

The idea of the "sandbox" is to provide a development environment with an IDE, a Python version with installed packages, compute power as well as capabilities for experiment tracking and model management. 

## Theia

Theia is an IDE that can be run in a Docker container. The script below pulls the image and runs the container.

```zsh
docker run -it --init -p 3000:3000 -v "$(pwd):/home/project:cached" theiaide/theia:latest
```

The Theia IDE should run on http://localhost:3000.

Theia can also be run for Python development. 

```zsh
docker run -it --init -p 3000:3000 -v "$(pwd):/home/project" theiaide/theia-python:latest
```

## MLflow Tracking

MLflow is a platform for the complete machine learning lifecycle. 

* https://mlflow.org

The training of models can be tracked with MLflow Tracking. In the `train.py` file a BernoulliNB classifier from Scikit-learn is trained on zoo data from the UCI ML Repository (https://archive.ics.uci.edu/ml/datasets/Zoo). The training run is tracked with MLflow and the results of the run (or several runs) can eventually be analyzed in the browser at http://127.0.0.1:5000 by running:

```zsh
mlflow ui
```