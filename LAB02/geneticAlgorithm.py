class geneticAlgorithm:
    def __init__(self, itMax=200, probCross=0.1,
                 probMut=0.1, populationSize=100,
                 evalSuccess=2000, evalFail=-1000,
                 successPos=2, successAcc=2):
        self._itMax = itMax
        self._probCross = probCross
        self._probMut = probMut
        self._populationSize = populationSize
        self._evalSuccess = evalSuccess
        self._evalFail = evalFail
        self._successPos = successPos
        self._successAcc = successAcc

    def get_parameters(self):
        return {"itMax": self._itMax,
                "probCross": self._probCross,
                "probMut": self._probMut,
                "populationSize": self._populationSize,
                "evalSuccess": self._evalSuccess,
                "evalFail": self._evalFail,
                "successPos": self._successPos,
                "successAcc": self._successAcc
                }

    def evaluation(self, f, population):
        output = []
        for unit in population:
            position, acc = f(unit)

            if position < self._successPos and abs(acc) < self._successAcc:
                score = self._evalSuccess - unit.count("1")
            else:
                score = self._evalFail

            output.append(unit, score)

        return output
