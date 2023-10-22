import random
import matplotlib.pyplot as plt
import numpy as np

from mySolver import mySolver


def stepLenDependency(f, fGradient, precision, stepLen, maxDepth, x0):

    results = []
    for index in range(1000):
        solverResult = mySolver(stepLen * (index + 1), precision, maxDepth).solve(f, fGradient, [x0])
        results.append(solverResult)

    return results


def plt_accuracy(results, expectedValue, title, stepLen):
    x = []
    y = []
    for index, result in enumerate(results):
        x.append(stepLen * (index + 1))
        y.append(abs(expectedValue - result[0][0]))
    plt.plot(x, y)
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
    plt.plot(x, y)
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


def randXMeasurements(f, fGradient, precision, stepLen, maxDepth, ammountRandX):
    randX = random.uniform(-2.9, 2.9)
    listX = [randX]
    results = stepLenDependency(f, fGradient, precision, stepLen, maxDepth, randX)
    for _ in range(ammountRandX - 1):
        randX = random.uniform(-2.9, 2.9)
        listX.append(randX)
        result = stepLenDependency(f, fGradient, precision, stepLen, maxDepth, randX)
        for index in range(1000):
            results[index][0][0] += result[index][0][0]/10
            results[index][1] += result[index][1]/ammountRandX
    return [results, listX]
