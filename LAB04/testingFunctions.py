import pandas as pd
from mySolver import MySolver
from copy import deepcopy
from sklearn.model_selection import train_test_split as tts
import matplotlib.pyplot as plt


def readCSV(filePath):
    df = pd.read_csv(filePath, delimiter=";")
    X = df.drop(["id", "cardio"], axis=1).values.tolist()
    Y = df["cardio"].values.tolist()
    return X, Y


def dataDiscretization(data):
    output = deepcopy(data)
    for line in output:
        line[0] = line[0] // 365
        line[2] = line[2] // 5
        line[3] = line[3] // 5
        line[4] = line[4] // 2
        line[5] = line[5] // 2
    return output


def getDepthAccuracy(depthLimit, X, Y):
    trainX, testX, trainY, testY = tts(X, Y, test_size=0.2)
    output = []
    for i in range(1, depthLimit + 1):
        solver = MySolver(i)
        solver.fit(trainX, trainY)
        predicted = solver.predict(testX)
        output.append(countCorrect(predicted, testY))
    return output


def pltAccuracy(data):
    x = []
    y = []
    for i, acc in enumerate(data):
        x.append(i + 1)
        y.append(acc)

    plt.scatter(x, y, s=5, c="red")
    plt.plot(x, y, linestyle="--", c="gray", linewidth=1, alpha=0.6)
    plt.xlabel("Depth")
    plt.ylabel("Accuracy in %")
    plt.title("Predicting accuracy for diffrent maximal depths")
    plt.show()


def countCorrect(Y1, Y2):
    return sum(1 for i in range(len(Y1)) if Y1[i] == Y2[i]) / len(Y2) * 100
