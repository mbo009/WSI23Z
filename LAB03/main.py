from two_player_games.games.connect_four import ConnectFour
from solver import miniMax
from connectFourNode import ConnectFourNode
from random import choice


def simulateGame(pOneParam=None, pTwoParam=None, mapSize=(7, 6)):
    game = ConnectFour(mapSize)
    while not game.is_finished():
        node = ConnectFourNode(game.state)
        playerParams = pOneParam if node.currentPlayer() == 1 else pTwoParam
        if not playerParams[0]:
            move = miniMax(node, playerParams[1], node.currentPlayer(),
                           playerParams[2], playerParams[3])[1]
        else:
            move = choice(game.state.get_moves())
        game.make_move(move)
    return game.get_winner()


def playAgainstBot(botParam, mapSize=(7, 6)):
    game = ConnectFour(mapSize)
    while not game.is_finished():
        if game.state.get_current_player().char == '1':
            print(game.state)
            print(" 1  2  3  4  5  6  7")
            moves = game.get_moves()
            userMove = -1

            while userMove < 0 or userMove > mapSize[1]:
                userMove = int(input("Wybierz kolumnę:")) - 1
            move = moves[userMove]
        else:
            node = ConnectFourNode(game.state)
            move = miniMax(node, botParam[0], 2,
                           botParam[1], botParam[2])[1]
        game.make_move(move)

    winner = game.get_winner()
    print(game.state)
    print(" 1  2  3  4  5  6  7")
    if winner is None:
        print('Draw!')
    else:
        print('Winner: Player ' + winner.char)


def simulateMultipleGames(gameCount, pOneParam, pTwoParam, mapSize=(7, 6)):
    winsPlayerOne = 0
    draws = 0
    for _ in range(gameCount):
        winner = simulateGame(pOneParam, pTwoParam, mapSize)
        if winner:
            if winner.char == '1':
                winsPlayerOne += 1
            else:
                draws += 1
    return winsPlayerOne, gameCount - winsPlayerOne - draws, draws


# print(simulateMultipleGames(1, [False, 3, 0, 20], [True, 3, 0, 20]))
