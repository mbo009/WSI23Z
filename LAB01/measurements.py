import random
import matplotlib.pyplot as plt
import numpy as np

from mySolver import mySolver


def stepLenDependency(f, fGradient, precision, stepLen,
                      maxDepth, x0, multipleX=False):

    results = []
    if multipleX is False:
        x0 = [x0]

    for index in range(1000):
        solverResult = mySolver(stepLen * (index + 1), precision,
                                maxDepth).solve(f, fGradient, x0)

        results.append(solverResult)

    return results


def plt_accuracy(results, expectedValue, title, stepLen, multipleX=False):
    x = []
    y = []
    for index, result in enumerate(results):
        x.append(stepLen * (index + 1))
        if multipleX is True:
            y.append(sum(abs(expectedValue[j] - result[0][j])
                         for j in range(len(expectedValue))))

        else:
            y.append(abs(expectedValue - result[0][0]))

    plt.scatter(x, y, s=1)
    plt.title(title)
    plt.xlabel("Długość kroku")
    plt.ylabel("Róźnica między wynikiem a wartością oczekiwaną")
    plt.show()


def plt_stepLen(results, title, stepLen):
    x = []
    y = []
    for index, result in enumerate(results):
        x.append(stepLen * (index + 1))
        y.append(result[1])
    plt.scatter(x, y, s=1)
    plt.title(title)
    plt.xlabel("Długość kroku")
    plt.ylabel("Ilość kroków")
    plt.show()


def plt_function(f, isGradient=False):
    x = np.linspace(-10, 10, 100)
    y = f([x])[0] if isGradient else f([x])
    plt.plot(x, y)
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.show()


def randX(rangeX, ammountX):
    if ammountX == 1:
        return random.uniform(rangeX[0], rangeX[1])
    else:
        return [random.uniform(rangeX[0], rangeX[1]) for _ in range(ammountX)]


def randXMeasurements(f, fGradient, precision, stepLen, maxDepth,
                      ammountRandX, rangeX, ammountX=1):

    drawnX = randX(rangeX, ammountX)
    listX = [drawnX]
    results = stepLenDependency(f, fGradient, precision, stepLen,
                                maxDepth, drawnX, (ammountX > 1))

    for _ in range(ammountRandX - 1):
        drawnX = randX(rangeX, ammountX)
        listX.append(drawnX)
        result = stepLenDependency(f, fGradient, precision, stepLen,
                                   maxDepth, drawnX, (ammountX > 1))
        for index in range(1000):
            results[index][0][0] += result[index][0][0]/ammountRandX
            results[index][1] += result[index][1]/ammountRandX

    return [results, listX]
