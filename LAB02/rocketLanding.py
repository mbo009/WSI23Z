def rocketLanding(unitMoves, baseMass=200, position=200, accParam=40,
                  deAccParam=0.09, successPos=2, successAcc=2,
                  successPoints=2000, failPoints=-1000):
    # acceleration
    acc = 0
    fuel = unitMoves.count("1")
    # base rocket + fuel mass
    mass = baseMass + fuel

    for move in unitMoves:
        if move == "0":
            acc -= deAccParam
        if move == "1":
            acc += accParam/mass - deAccParam
            mass -= 1

        position += acc
        if position < successPos:
            if position > 0 and abs(acc) < successAcc:
                return successPoints - fuel
            return failPoints - fuel

    if position < successPos and position > 0 and abs(acc) < successAcc:
        return successPoints - fuel
    return failPoints - fuel
