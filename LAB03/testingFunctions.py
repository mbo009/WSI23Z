from two_player_games.games.connect_four import ConnectFour
from solver import miniMax
from connectFourNode import ConnectFourNode
from random import choice
import matplotlib.pyplot as plt
import pandas as pd


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


def analyzeMovesQuality(depth, mapSize=(6, 7)):
    game = ConnectFour(mapSize)
    quality = [[] for _ in range(depth)]
    moves = [[] for _ in range(depth)]
    while not game.is_finished():
        node = ConnectFourNode(game.state)
        if node.currentPlayer() == 1:
            for i in range(depth):
                minimaxData = miniMax(node, i+1, 1)
                quality[i].append(minimaxData[0])
                moves[i].append(minimaxData[1])
            move = moves[depth-1][-1]
        else:
            move = miniMax(node, depth, 1)[1]
        game.make_move(move)
    return quality, moves


def pltMoveValues(moveValuesArr, colorsArray, title,
                  addLines=False, indexShift=0):
    x = []
    y = []
    firstIt = True
    for i, moveValues in enumerate(moveValuesArr):
        for j, value in enumerate(moveValues):
            if firstIt:
                x.append(j)
            y.append(value)

        plt.scatter(x, y, c=colorsArray[i], s=5,
                    label=f'Depth: {i + 1 + indexShift}')
        if addLines:
            plt.plot(x, y, c=colorsArray[i], linestyle='--',
                     linewidth=1, alpha=0.5)
        y.clear()
        firstIt = False

    plt.xlabel("Move number")
    plt.ylabel("Score")
    plt.title(title)
    plt.legend()
    plt.show()


def prepareMovesTable(movesArr):
    rows = []
    for i in range(len(movesArr[0])):
        data = []
        for j in range(len(movesArr)):
            data.append(movesArr[j][i].column)
        rows.append(data)

    columns = pd.DataFrame([
                        ["Moves picked by minimax with depth:", 1],
                        ["Moves picked by minimax with depth:", 2],
                        ["Moves picked by minimax with depth:", 3],
                        ["Moves picked by minimax with depth:", 4],
                        ["Moves picked by minimax with depth:", 5],
                        ["Moves picked by minimax with depth:", 6]],
                        columns=["Iteration", ""])
    columns = pd.MultiIndex.from_frame(columns)

    df = pd.DataFrame(rows, columns=columns)
    df.index = df.index + 1
    df = df.style.set_table_styles([
        {'selector': 'td', 'props': [('text-align', 'center')]},
        {'selector': 'th', 'props': [('text-align', 'center')]}
    ])
    return df

# print(simulateMultipleGames(1, [False, 3, 0, 20], [True, 3, 0, 20]))
