from solver import Solver
from math import exp
from copy import copy


class mySolver(Solver):

    def __init__(self, stepLen=0.001, precision=0.1, maxDepth=100):
        self._stepLen = stepLen
        self._maxDepth = maxDepth
        self._precision = precision

    def get_parameters(self):
        return {"stepLen": self._stepLen,
                "maxDepth": self._maxDepth,
                "precision": self._precision}

    def solve(self, f, fGradient, x0):
        depth = 1
        nextX = x0
        stepLen = copy(self._stepLen)

        while (depth <= self._maxDepth):

            currentX = copy(nextX)
            fGradientValue = fGradient(currentX)

            for index in range(len(x0)):
                nextX[index] = (currentX[index] - stepLen * fGradientValue[index])

            if (sum(abs(value) for value in fGradientValue) <= self._precision or
               all(abs(nextX[index] - currentX[index]) <= self._precision for index in range(len(x0)))):
                return nextX

            if (f(nextX) >= f(currentX)):
                stepLen /= 2

            depth += 1
        return nextX


def f(x):
    return 1/4*pow(x[0], 4)


def fGradient(x):
    return [pow(x[0], 3)]


def g(x):
    return 1.5 - exp(-pow(x[0], 2) - pow(x[1], 2)) - 0.5 * exp(- pow(x[0] - 1, 2) - pow(x[1] + 2, 2))


def gGradient(x):
    return [2 * x[0] * exp(-pow(x[0], 2) - pow(x[1], 2)) + (x[0] - 1) * exp(- pow(x[0] - 1, 2) - pow(x[1] + 2, 2)),
            2 * x[1] * exp(-pow(x[0], 2) - pow(x[1], 2)) + (x[1] - 1) * exp(- pow(x[0] - 1, 2) - pow(x[1] + 2, 2))]


solver = mySolver(0.01, 1e-30, 1e10)

# print(solver.solve(f, fGradient, [-4]))
print(solver.solve(g, gGradient, [3.5, 3.5]))
