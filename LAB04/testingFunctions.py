import pandas as pd
from mySolver import MySolver
from copy import deepcopy
from sklearn.model_selection import train_test_split as tts
import matplotlib.pyplot as plt
import random


def readCSV(filePath):
    df = pd.read_csv(filePath, delimiter=";")
    X = df.drop(["id", "cardio"], axis=1).values.tolist()
    Y = df["cardio"].values.tolist()
    return X, Y


def checkAccuracy(X, Y, depth, rangeL, rangeR):
    output = []
    solver = MySolver(depth)
    solver.fit(X, Y)
    x = deepcopy(X)
    for i in range(rangeL, rangeR):
        if i > 0:
            x = addRandData(X, i)
        elif i < 0:
            x = cutData(X, -i)
        output.append(countCorrect(solver.predict(x), Y))
    return output


def addRandData(data, addColCount):
    output = []
    for line in data:
        newLine = line + [random.randint(1, 10) for _ in range(addColCount)]
        output.append(newLine)
    return output


def cutData(data, rmColCount):
    output = []
    for line in data:
        newLine = line[:-rmColCount]
        output.append(newLine)
    return output


def dataDiscretization(data):
    output = deepcopy(data)
    for line in output:
        line[0] = line[0] // 365
        line[2] = line[2] // 5
        line[3] = line[3] // 5
        line[4] = line[4] // 2
        line[5] = line[5] // 2
    return output


def getDepthAccuracy(depthLimit, X, Y, seed, returnTraining=False, testSize=0.2):
    trainX, testX, trainY, testY = tts(X, Y, test_size=testSize, random_state=seed)
    predicted = []
    predictedTrain = []
    for i in range(1, depthLimit + 1):
        solver = MySolver(i)
        solver.fit(trainX, trainY)
        predicted.append(countCorrect(solver.predict(testX), testY))
        if returnTraining:
            predictedTrain.append(countCorrect(solver.predict(trainX), trainY))

    return [predicted, predictedTrain]


def pltAccuracy(
    dataArr, labels=["Testing dataset", "Training dataset"], colorsArray=["red", "blue"]
):
    x = []
    y = []
    firstIt = True
    for i, data in enumerate(dataArr):
        for j, acc in enumerate(data):
            if firstIt:
                x.append(j + 1)
            y.append(acc)
        plt.scatter(x, y, s=5, c=colorsArray[i], label=labels[i])
        plt.plot(x, y, linestyle="--", c="gray", linewidth=1, alpha=0.6)
        y.clear()
        firstIt = False

    plt.xlabel("Depth")
    plt.ylabel("Accuracy in %")
    plt.title("Predicting accuracy for diffrent maximal depths")
    plt.legend()
    plt.show()


def countCorrect(Y1, Y2):
    return sum(1 for i in range(len(Y1)) if Y1[i] == Y2[i]) / len(Y2) * 100
