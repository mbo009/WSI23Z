from copy import deepcopy


class Node:
    def __init__(self, state):
        self.state = state

    def currentPlayer(self):
        return int(self.state.get_current_player().char)

    def evaluate(self, player):
        winner = self.state.get_winner()
        if winner:
            winner = int(winner.char)
            return 10000 if winner == player else -10000
        else:
            directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
            points = 0
            for length in (3, 2):
                for direction in directions:
                    points += self._countNotBlocked(length, direction, player)
                if length == 3:
                    points *= 5
        return points

    def getChildrenStates(self):
        children = []
        possibleMoves = self.state.get_moves()
        for move in possibleMoves:
            newChild = deepcopy(self.state).make_move(move)
            children.append(Node(newChild))
        return children

    def getPossibleMoves(self):
        return self.state.get_moves()

    def isTerminal(self):
        return (self.state.is_finished() or self.state.get_moves is None)

    def _countNotBlocked(self, length, move_cords, player):
        isColMovingLeft = 1 if move_cords[0] == -1 else 0
        isRowMovingLeft = 1 if move_cords[1] == -1 else 0
        count = 0
        for column in range(len(self.state.fields) - move_cords[0] * 3):
            for row in range(len(self.state.fields[column])
                             - abs(move_cords[1]) * 3):
                count += self._check(length, (column + 3 * isColMovingLeft,
                                     row + 3 * isRowMovingLeft),
                                     move_cords, player)
        return count

    def _check(self, length, start_coords, move_coords, player):
        fields = []
        for i in range(4):
            row = start_coords[0] + move_coords[0] * i
            col = start_coords[1] + move_coords[1] * i
            field = self.state.fields[row][col]
            if field:
                field = int(field.char)
            fields.append(field)

        if fields.count(player) != length:
            return 0

        count = sum(1 for i in range(4 - length) if not fields[i])
        if count == 4 - length:
            return 1
        return 0 if any(fields[i] for i in range(length, 4)) else 1


def miniMax(node: Node, depth: int, maximizingPlayer: int,
            a=float('-inf'), b=float('inf')):
    if depth == 0 or node.isTerminal():
        return node.evaluate(maximizingPlayer), None

    moves = node.getPossibleMoves()
    move = None

    if node.currentPlayer() == maximizingPlayer:
        value = float('-inf')
        for index, child in enumerate(node.getChildrenStates()):
            miniMaxOutput = miniMax(child, depth - 1, maximizingPlayer, a, b)
            if miniMaxOutput[0] > value:
                value = miniMaxOutput[0]
                move = moves[index]
            a = max(a, value)
            if value >= b:
                break
    else:
        value = float('inf')
        for index, child in enumerate(node.getChildrenStates()):
            miniMaxOutput = miniMax(child, depth - 1, maximizingPlayer, a, b)
            if miniMaxOutput[0] < value:
                value = miniMaxOutput[0]
                move = moves[index]
            b = min(b, value)
            if value <= a:
                break
    return value, move
