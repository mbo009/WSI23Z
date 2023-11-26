from two_player_games.games.connect_four import ConnectFour
from solver import Node, miniMax


game = ConnectFour()
while not game.is_finished():
    moves = game.get_moves()
    if game.state.get_current_player().char == '1':
        print(game.state)
        print(" 1  2  3  4  5  6  7")
        move = moves[int(input("W którą kolumnę chcesz wykonać ruch:")) - 1]
    else:
        node = Node(game.state)
        move = miniMax(node, 4, 2)[1]
    game.make_move(move)

winner = game.get_winner()
if winner is None:
    print('Draw!')
else:
    print('Winner: Player ' + winner.char)
