import random
import matplotlib.pyplot as plt
import numpy as np

from mySolver import mySolver
import functions


def stepLenDependency(f, fGradient, precision, maxDepth):

    results = []
    steps = [1e-10, 1e-5, 1e-3, 1e-2, 0.1, 0.2, 0.3, 0.4, 0.5]
    for step in steps:
        solverResult = mySolver(step, precision, maxDepth).solve(f, fGradient, [2])
        print(solverResult)
        results.append([step, solverResult[1]])

    return results


def plt_stepLen(results, title):
    x = []
    y = []
    for result in results:
        x.append(result[0])
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


# plt_function(functions.fGradient, True)
# plt_stepLen(stepLenDependency(functions.f, functions.fGradient, 1e-3, 1e6),"Wykres")
