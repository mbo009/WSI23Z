from solver import Solver
from copy import copy
import numpy as np


class MySolver(Solver):
    def get_params(self, deep=True):
        return {}

    def fit(self, X, y):
        self._cls, clsCount = np.unique(y, return_counts=True)
        self._probCls = [count / len(y) for count in clsCount]
        self._meanCls = []
        self._stdCls = []

        for cls in self._cls:
            meanArr = []
            stdArr = []
            x = X[y == cls]
            for i in range(X.shape[1]):
                meanArr.append(np.mean(x[:, i]))
                stdArr.append(np.std(x[:, i]))
            self._meanCls.append(copy(meanArr))
            self._stdCls.append(copy(stdArr))

    def predict(self, X):
        predicted = []

        for x in X:
            probabilities = []
            for i in range(len(self._cls)):
                prob = 1.0
                for j in range(X.shape[1]):
                    prob *= (1 / (np.sqrt(2 * np.pi) * self._stdCls[i][j])) * np.exp(
                        -0.5 * ((x[j] - self._meanCls[i][j]) / self._stdCls[i][j]) ** 2
                    )
                probabilities.append(prob * self._probCls[i])

            predicted.append(self._cls[np.argmax(probabilities)])

        return np.array(predicted)
