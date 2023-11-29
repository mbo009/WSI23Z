from random import choice
from node import Node


def miniMax(node: Node, depth: int, maximizingPlayer: int,
            a=float('-inf'), b=float('inf')):
    if depth == 0 or node.isTerminal():
        return node.evaluate(maximizingPlayer), None

    moves = node.getPossibleMoves()
    bestMoves = []

    if node.currentPlayer() == maximizingPlayer:
        value = float('-inf')
        for index, child in enumerate(node.getChildrenStates()):
            miniMaxOutput = miniMax(child, depth - 1, maximizingPlayer, a, b)

            if miniMaxOutput[0] > value:
                value = miniMaxOutput[0]
                bestMoves.clear()
            if miniMaxOutput[0] == value:
                bestMoves.append(moves[index])

            a = max(a, value)
            if value >= b:
                break
    else:
        value = float('inf')
        for index, child in enumerate(node.getChildrenStates()):
            miniMaxOutput = miniMax(child, depth - 1, maximizingPlayer, a, b)

            if miniMaxOutput[0] < value:
                value = miniMaxOutput[0]
                bestMoves.clear()
            if miniMaxOutput[0] == value:
                bestMoves.append(moves[index])

            b = min(b, value)
            if value <= a:
                break

    return value, choice(bestMoves)
