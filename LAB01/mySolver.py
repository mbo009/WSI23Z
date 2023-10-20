class mySolver():

    def __init__(self, startingX=0, stepLen=0.001, precision=0.1, maxDepth=100):
        self._startingX = startingX
        self._stepLen = stepLen
        self._maxDepth = maxDepth
        self._precision = precision

    def get_parameters(self):
        return {"startingX": self._startingX,
                "stepLen": self._stepLen}

    def solve(self, f, fGradient, stepLen=0.1):
        depth = 1
        nextX = self._startingX

        while (depth <= self._maxDepth):

            currentX = nextX
            nextX = currentX - stepLen * fGradient(currentX)

            if (abs(fGradient(currentX)) <= self._precision and abs(nextX - currentX) <= self._precision):
                return nextX

            if (f(nextX) >= f(currentX)):
                stepLen /= 2

            depth += 1

        return nextX


def f(x):
    return 1/4*pow(x, 4)


def fGradient(x):
    return pow(x, 3)


solver = mySolver(0, 0.01, 0.01, 1000)

print(solver.solve(f, fGradient, 0.1))
