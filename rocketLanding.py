def rocketLanding(unitMoves, baseMass=200, position=200, accParam=40, deAccParam=0.09):
    # acceleration
    acc = 0
    # base rocket + fuel mass
    mass = baseMass + unitMoves.count("1")

    for move in unitMoves:
        if move == "0":
            acc -= deAccParam
        if move == "1":
            acc += accParam/mass
            mass -= 1

        position += acc

        if position < 0:
            return position, acc

    return position, acc
