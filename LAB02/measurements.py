import matplotlib.pyplot as plt

from rocketLanding import rocketLanding
from gaSolver import gaSolver


def getSolverHistories(paramsArray, itMax, numOfStarts=25):
    avgHist = []
    BSHist = []
    currentBSHist = []
    currentAvgHist = []
    bestScores = []
    currentBestScores = []

    for params in paramsArray:
        for _ in range(numOfStarts):
            solver = gaSolver(itMax, params[0],
                              params[1], params[2])
            data = solver.solve(rocketLanding, solver.populationInit(),
                                True, True)
            currentBSHist.append(data[2])
            currentAvgHist.append(data[3])
            currentBestScores.append(data[1])
        BSHist.append([sum(x) / numOfStarts for x in zip(*currentBSHist)])
        avgHist.append([sum(x) / numOfStarts for x in zip(*currentAvgHist)])
        bestScores.append(sum(currentBestScores) / numOfStarts)
        currentBSHist.clear()
        currentAvgHist.clear()
        currentBestScores.clear()
    return BSHist, avgHist, bestScores


def plotHistories(histories, paramsArray, colorsArray,
                  title, zoomState=0, addLines=False):
    x = []
    y = []
    values = []
    firstIt = True
    for i, history in enumerate(histories):
        for j, itScore in enumerate(history):
            if firstIt:
                x.append(j)
            y.append(itScore)
            if ((zoomState == -1 and itScore <= -1000) or
               (zoomState == 1 and itScore >= 1800)):
                values.append(itScore)

        plt.scatter(x, y, c=colorsArray[i], s=2,
                    label=f'CrossProb: {paramsArray[i][0]}, ' +
                          f'MutProb: {paramsArray[i][1]}, ' +
                          f'PopSize: {paramsArray[i][2]}')
        if addLines:
            plt.plot(x, y, c=colorsArray[i], linestyle='--',
                     linewidth=0.5, alpha=0.5)
        y.clear()
        firstIt = False

    plt.xlabel("Iteration")
    plt.ylabel("Score")
    plt.legend(prop={'size': 4})
    plt.title(title)

    # Zoom state tells us:
    #  1 - Zoom at the top
    #  0 - No zoom
    # -1 - Zoom at the bottom
    if zoomState == 1:
        plt.ylim(min(values) - 2, max(values) + 2)
    elif zoomState == -1:
        plt.ylim(min(values) - 2, max(values) + 2)

    plt.show()
