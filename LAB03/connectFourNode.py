from copy import deepcopy
from node import Node


class ConnectFourNode(Node):
    def __init__(self, state):
        super().__init__(state)

    def currentPlayer(self):
        return int(self.state.get_current_player().char)

    def evaluate(self, player):
        winner = self.state.get_winner()
        if winner:
            winner = int(winner.char)
            return float('inf') if winner == player else float('-inf')
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
            children.append(ConnectFourNode(newChild))
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
