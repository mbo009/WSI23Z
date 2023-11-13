import random


class gaSolver:
    def __init__(self, itMax=1000, probCross=0.01,
                 probMut=0.01, populationSize=100,
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
        scores = []
        for unit in population:
            scores.append(f(unit))

        return scores

    def findBest(self, population, scores):
        index = scores.index(max(scores))
        return population[index], scores[index]

    def populationInit(self):
        population = []
        for _ in range(self._populationSize):
            population.append("".join(random.choice("01") for _ in range(self._unitSize)))
        return population

    def selection(self, population, scores):
        probIntervals = []
        newPopulation = []
        lastScore = 0

        for score in scores:
            probIntervals.append(score + self._scalingConstant + lastScore)
            lastScore += score + self._scalingConstant

        for _ in range(len(population)):
            drawnNum = random.randint(0, lastScore)
            leftEnd = probIntervals[0]

            if drawnNum <= leftEnd:
                newPopulation.append(population[0])
            else:
                for i in range(1, len(population)):
                    if drawnNum > leftEnd and drawnNum <= probIntervals[i]:
                        newPopulation.append(population[i])
                        break
                    leftEnd = probIntervals[i]

        return newPopulation

    def mutation(self, population):
        mutatedPopulation = []

        for unit in population:
            mutatedUnit = ""
            for index in range(self._unitSize):
                drawnNum = random.random()
                if drawnNum < self._probMut:
                    mutatedUnit += "1" if unit[index] == "0" else "0"
                else:
                    mutatedUnit += unit[index]
            mutatedPopulation.append(mutatedUnit)

        return mutatedPopulation

    def crossing(self, population):
        newPopulation = []
        pairFormed = False
        leftUnit = ""

        for unit in population:
            if pairFormed:
                drawnPoint = random.randint(1, self._unitSize - 2)
                newPopulation.append(leftUnit[:drawnPoint] + unit[drawnPoint:])
                newPopulation.append(unit[:drawnPoint] + leftUnit[drawnPoint:])
            else:
                leftUnit = unit

            pairFormed = not pairFormed

        return newPopulation

    def solve(self, problem, pop0, returnBSHistory=False,
              returnAvgHistory=False):
        bestScoreHistory = []
        avgHistory = []

        t = 0
        scores = self.evaluation(problem, pop0)
        bestUnit, bestScore = self.findBest(pop0, scores)
        population = pop0

        while t < self._itMax:
            selectedPop = self.selection(population, scores)
            mutatedPop = self.mutation(self.crossing(selectedPop))
            scores = self.evaluation(problem, mutatedPop)

            newBestUnit, newBestScore = self.findBest(mutatedPop, scores)
            if newBestScore > bestScore:
                bestScore = newBestScore
                bestUnit = newBestUnit

            if returnBSHistory:
                bestScoreHistory.append(newBestScore)
            if returnAvgHistory:
                avgHistory.append(round(sum(scores)/len(scores)))
            population = mutatedPop
            t += 1

        if returnBSHistory:
            if returnAvgHistory:
                return bestUnit, bestScore, bestScoreHistory, avgHistory
            return bestUnit, bestScore, bestScoreHistory
        elif returnAvgHistory:
            return bestUnit, bestScore, avgHistory
        return bestUnit, bestScore
