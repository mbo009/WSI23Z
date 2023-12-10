from solver import Solver
from id3Node import ID3Node
import numpy as np


class MySolver(Solver):
    def __init__(self, depthLimit=2, minSampleLimit=2, root=None):
        self._minSampleLimit = minSampleLimit
        self._depthLimit = depthLimit
        self.root = root
        super().__init__()

    def get_parameters(self):
        return {"split_count": self._minSampleLimit, "depth": self._depthLimit}

    def _split(self, X, Y, index, threshold):
        left = [[], []]
        right = [[], []]
        for i, row in enumerate(X):
            if row[index] <= threshold:
                left[0].append(row)
                left[1].append(Y[i])
            else:
                right[0].append(row)
                right[1].append(Y[i])
        return left, right

    def _entropy(self, y):
        values = list(set(y))
        entropy = 0
        for value in values:
            prob = y.count(value) / len(y)
            entropy += -prob * np.log2(prob)
        return entropy

    def _infGain(self, parentY, leftY, rightY):
        weightLeft = len(leftY) / len(parentY)
        weightRight = len(rightY) / len(parentY)
        return (
            self._entropy(parentY)
            - weightLeft * self._entropy(leftY)
            - weightRight * self._entropy(rightY)
        )

    def _best_split(self, X, Y, sampleCount, columnsCount):
        bestSplit = ID3Node()
        maxInfGain = float("-inf")
        for index in range(columnsCount):
            values = list(set(row[index] for row in X))
            for i, value in enumerate(values):
                left, right = self._split(X, Y, index, value)
                if len(left) > 0 and len(right) > 0:
                    infGain = self._infGain(Y, left[1], right[1])
                    if infGain > maxInfGain:
                        bestSplit = ID3Node(
                            index,
                            value,
                            left,
                            right,
                            infGain,
                        )
                        maxInfGain = infGain
        return bestSplit

    def buildTree(self, X, y, currentDepth=0):
        sampleCount, columnsCount = np.shape(X)
        if currentDepth <= self._depthLimit:
            bestSplit = self._best_split(X, y, sampleCount, columnsCount)
            if bestSplit.infGain > 0:
                left = self.buildTree(
                    bestSplit.left[0], bestSplit.left[1], currentDepth + 1
                )
                right = self.buildTree(
                    bestSplit.right[0], bestSplit.right[1], currentDepth + 1
                )
                return ID3Node(
                    bestSplit.featureIndex,
                    bestSplit.threshold,
                    left,
                    right,
                    bestSplit.infGain,
                )
        return ID3Node(value=max(y, key=y.count))

    def fit(self, X, y):
        self.root = self.buildTree(X, y)

    def makePrediction(self, X, tree):
        if tree.value is not None:
            return tree.value
        featureValue = X[tree.featureIndex]
        if featureValue <= tree.threshold:
            return self.makePrediction(X, tree.left)
        else:
            return self.makePrediction(X, tree.right)

    def predict(self, X):
        return [self.makePrediction(sample, self.root) for sample in X]
