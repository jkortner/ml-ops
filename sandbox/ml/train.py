import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score
import pandas as pd


def get_X_y(df, target):

    # sklearn split
    train, test = train_test_split(df)

    # X, y split
    X_train = train.drop([target], axis=1)
    X_test  = test.drop([target], axis=1)
    y_train = train[[target]]
    y_test  = test[[target]]

    return X_train, X_test, y_train, y_test


def metrics(y, y_hat):

    accuracy = accuracy_score(y, y_hat)

    return accuracy


if __name__ == "__main__":
    # get zoo.data from:
    # https://archive.ics.uci.edu/ml/datasets/Zoo
    # COLS = ["name", "hair", "feathers", "eggs", "milk", "airborne", "aquatic", 
    #         "predator", "toothed", "backbone", "breathes", "venomous", "fins", 
    #         "legs", "tail", "domestic", "catsize", "class"]
    # DF = pd.read_csv('zoo.data', sep = ',', names=COLS)
    # print(DF)
    # DF.to_csv('zoo.csv', index=False)

    # load zoo.csv
    df = pd.read_csv('zoo.csv')
    df = df.drop(columns=['name'])
    
    # split df into training and test sets
    X_train, X_test, y_train, y_test = get_X_y(df, 'class')

    with mlflow.start_run():

        clf = BernoulliNB()
        clf.fit(X=X_train, y=y_train.values.ravel())

        y_hat = clf.predict(X_test)

        accuracy = metrics(y_test, y_hat)
        print('Accuracy: %s' % accuracy)

        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(clf, "model")
