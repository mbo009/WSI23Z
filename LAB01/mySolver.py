from solver import Solver
from copy import copy


class mySolver(Solver):

    def __init__(self, stepLen=0.001, precision=0.1, maxDepth=100, modulationRate=64):
        self._stepLen = stepLen
        self._maxDepth = maxDepth
        self._precision = precision
        self._modulationRate = modulationRate

    def get_parameters(self):
        return {"stepLen": self._stepLen,
                "maxDepth": self._maxDepth,
                "precision": self._precision,
                "modulationRate": self._modulationRate}

    def solve(self, f, fGradient, x0, isReturningPath=False):
        depth = 1
        nextX = copy(x0)
        path = []
        path.append([copy(nextX), [f(nextX)]])
        stepLen = copy(self._stepLen)

        while (depth <= self._maxDepth):
            depth += 1
            currentX = copy(nextX)
            fGradientValue = fGradient(currentX)

            for index in range(len(x0)):
                nextX[index] = (currentX[index]
                                - stepLen * fGradientValue[index])
            if isReturningPath:
                path.append([copy(nextX), [f(nextX)]])

            if (sum(abs(value) for value in fGradientValue) <= self._precision
                or all(abs(nextX[index] - currentX[index]) <= self._precision
                       for index in range(len(x0)))):
                return ([nextX, depth, path] if isReturningPath
                        else [nextX, depth])

            if (f(nextX) >= f(currentX)):
                stepLen /= self.modulationRate
        return [nextX, depth, path] if isReturningPath else [nextX, depth]
