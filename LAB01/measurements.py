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


def plt_function(f, isGradient=False, width=10,
                 additionalPoints=None, colors=None):
    x = np.linspace(-width, width, 100)
    y = f([x])[0] if isGradient else f([x])

    if additionalPoints:
        for index, setOfPoints in enumerate(additionalPoints):
            additional_x, additional_y = zip(*setOfPoints)
            plt.scatter(additional_x, additional_y,
                        c=colors[index % len(colors)], marker='o',
                        label=f"x0 = {additional_x[0]}", s=15)

    plt.plot(x, y)
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)
    plt.legend()
    plt.show()


def plt_function3D(f, additionalPoints=None, pointsColors=None,
                   pltCmap='PiYG', visibility=1):
    x1 = np.linspace(-2, 2, 100)
    x2 = np.linspace(-2, 2, 100)
    x1, x2 = np.meshgrid(x1, x2)
    y = np.zeros_like(x1)

    for i in range(x1.shape[0]):
        for j in range(x1.shape[1]):
            y[i, j] = f([x1[i, j], x2[i, j]])

    figure = plt.figure()
    plot = figure.add_subplot(111, projection='3d')
    plot.plot_surface(x1, x2, y, cmap=pltCmap, alpha=visibility)

    if additionalPoints:
        for index, setOfPoints in enumerate(additionalPoints):
            additionalX, additionalY = zip(*setOfPoints)
            additionalX1, additionalX2 = zip(*additionalX)
            plot.scatter(additionalX1, additionalX2, additionalY,
                         c=pointsColors[index % len(pointsColors)],
                         s=100, label=f"x1, x2 = {additionalX[0]}")

    plot.set_xlabel('x1')
    plot.set_ylabel('x2')
    plot.set_zlabel('g(x1, x2)')
    plot.set_title('3D Plot of g(x1, x2)')

    plt.legend()
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
