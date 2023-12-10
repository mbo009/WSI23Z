import pandas as pd
from mySolver import MySolver
from copy import deepcopy


def readCSV(filePath):
    df = pd.read_csv(filePath, delimiter=";")
    X = df.drop(["id", "cardio"], axis=1).values.tolist()
    Y = df["cardio"].values.tolist()
    return X, Y


def dataDiscretization(data):
    output = deepcopy(data)
    for line in output:
        line[0] = line[0] // 365
        line[2] = line[2] // 10
        line[3] = line[3] // 5
        line[4] = line[4] // 2
        line[5] = line[5] // 2
    return output


def countCorrect(Y1, Y2):
    return sum(1 for i in range(len(Y1)) if Y1[i] == Y2[i])


if __name__ == "__main__":
    X, Y = readCSV("cardio_train.csv")
    X = dataDiscretization(X)
    solver = MySolver(depthLimit=10)
    solver.fit(X[:20000], Y[:20000])
    Y1 = Y[20000:20050]
    Y2 = solver.predict(X[20000:20050])
    print(countCorrect(Y1, Y2))
