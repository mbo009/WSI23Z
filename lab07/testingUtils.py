import pandas as pd
from mySolver import MySolver
import numpy as np
from sklearn.model_selection import train_test_split as tts
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score, KFold
import matplotlib.pyplot as plt

# from mySolver import MySolver
# import random


def readCSV(filePath):
    df = pd.read_csv(filePath, delimiter=";")
    X = df.drop(["id", "cardio"], axis=1).values
    Y = df["cardio"].values

    return X, Y


def compareAccuracy(X, Y, itCount, testSize):
    accMySolver = []
    accSKSolver = []
    for _ in range(itCount):
        trainX, testX, trainY, testY = tts(X, Y, test_size=testSize)
        solver = MySolver()
        solver.fit(trainX, trainY)
        yPred = solver.predict(testX)
        accMySolver.append(np.sum(testY == yPred) / len(testY) * 100)
        solver = GaussianNB()
        solver.fit(trainX, trainY)
        yPred = solver.predict(testX)
        accSKSolver.append(np.sum(testY == yPred) / len(testY) * 100)

    return (
        np.mean(accMySolver),
        np.mean(accSKSolver),
        np.std(accMySolver),
        np.std(accSKSolver),
    )


def crossVal(X, y, k):
    kf = KFold(n_splits=k, shuffle=True)

    return sum(cross_val_score(MySolver(), X, y, cv=kf, scoring="accuracy")) / k * 100


def getCrossValData(X, y, kLimit, itCount):
    data = []
    for k in range(2, kLimit):
        tmp = []
        for _ in range(itCount):
            tmp.append(crossVal(X, y, k))
        data.append([np.mean(tmp), np.std(tmp)])

    return data


def getValData(X, y, splits, itCount):
    data = []
    for split in splits:
        tmp = []
        for _ in range(itCount):
            trainX, testX, trainY, testY = tts(X, y, test_size=split)
            solver = MySolver()
            solver.fit(trainX, trainY)
            yPred = solver.predict(testX)
            tmp.append(np.sum(testY == yPred) / len(testY) * 100)
        data.append([np.mean(tmp), np.std(tmp)])

    return data


def pltAcc(X, scores, title, xlabel, ylabel):
    x = [str(np.round(label, 1)) for label in X]
    y, deviations = zip(*scores)
    plt.bar(x, y, yerr=deviations, color="blue", capsize=3)
    for i, acc in enumerate(y):
        plt.text(
            i,
            min(y) - 0.5,
            f"{acc:.2f}%",
            ha="center",
            va="bottom",
            color="white",
            fontsize=6,
        )

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylim(50, 65)
    plt.ylabel(ylabel)
    plt.show()
