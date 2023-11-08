import random


class gaSolver:
    def __init__(self, itMax=200, probCross=0.1,
                 probMut=0.1, populationSize=100,
                 unitSize=200, scalingConstant=1201):
        self._itMax = itMax
        self._probCross = probCross
        self._probMut = probMut
        self._populationSize = populationSize
        self._unitSize = unitSize
        self._scalingConstant = scalingConstant

    def getParameters(self):
        return {"itMax": self._itMax,
                "probCross": self._probCross,
                "probMut": self._probMut,
                "populationSize": self._populationSize,
                "unitSize": self._unitSize
                }

    def evaluation(self, f, population):
        output = []
        for unit in population:
            output.append(f(unit))

        return output

    def findBest(self, population, scores):
        index = scores.index(max(scores))
        return population[index], scores[index]

    def populationInit(self):
        population = []
        for _ in range(self._populationSize):
            population.append("".join(random.choice("01") for _ in range(self._unitSize)))

    def selection(self, population, scores):
        probIntervals = []
        newPopulation = []
        lastScore = 0
        for score in scores:
            probIntervals.append(score + self._scalingConstant + lastScore)
            lastScore += score + self._scalingConstant

        for _ in range(population):
            drawnNum = random.randint(0, lastScore)
            leftEnd = probIntervals[0]

            if drawnNum < leftEnd:
                newPopulation.append(population[0])
            else:
                for i in range(1, population):
                    if leftEnd > drawnNum and probIntervals[i] <= drawnNum:
                        newPopulation.append(population[i])
        return newPopulation

    def mutation(self, population):
        pass
