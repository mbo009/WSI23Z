import matplotlib.pyplot as plt

from rocketLanding import rocketLanding
from geneticAlgorithm import gaSolver


def getBSHistories(paramsArray, itMax):
    BSHistories = []
    for params in paramsArray:
        solver = gaSolver(itMax, params[0],
                          params[1], params[2])
        BSHistories.append(solver.solve(rocketLanding,
                                        solver.populationInit(), True)[2])
    return BSHistories


def plotBSHistories(BSHistories, paramsArray, colorsArray, zoomState=0):
    x = []
    y = []
    values = []
    firstIt = True
    for i, BSHistory in enumerate(BSHistories):
        for j, bestItScore in enumerate(BSHistory):
            if firstIt:
                x.append(j)
            y.append(bestItScore)
            if ((zoomState == -1 and bestItScore <= -1000) or
               (zoomState == 1 and bestItScore >= 1800)):
                values.append(bestItScore)

        plt.scatter(x, y, c=colorsArray[i], s=1,
                    label=f'Crossing prob: {paramsArray[i][0]}, ' +
                          f'Mutation prob: {paramsArray[i][1]}, ' +
                          f'Pop size: {paramsArray[i][2]}')
        y.clear()
        firstIt = False

    plt.xlabel("Iteration")
    plt.ylabel("Score")
    plt.legend(prop={'size': 7})

    # Zoom state tells us:
    #  1 - Zoom at the top
    #  0 - No zoom
    # -1 - Zoom at the bottom
    if zoomState == 1:
        plt.ylim(min(values) - 5, max(values) + 5)
        plt.title("Best score in each iteration(top scores)")
    elif zoomState == -1:
        plt.ylim(min(values) - 5, max(values) + 5)
        plt.title("Best score in each iteration(bottom scores)")
    else:
        plt.title("Best score in each iteration")

    plt.show()


paramsArray = [[0.1, 0.001, 100], [0.001, 0.001, 100], [0.005, 0.005, 100]]
colorsArray = ["red", "blue", 'green']
BSHistories = getBSHistories(paramsArray, 500)
