from game import *
from player import *
from network import *
from tqdm import tqdm

import numpy as np
import time

##########
def printGame(board, winner):
    print board
    if (winner != 0):
        print "\nPlayer {0} won!".format(winner)
        
    else:
        print "\nThe game was a draw. (Boring!)"
#########

'''
    DEFINE PLAYERS AND NETWORKS
'''

#net11 = Network("Endstate1", [3, 6, 7], 0.01)
#net12 = Network("MonteCarlo1", [3, 6, 7], 0.01)
net13 = Network("Qlearning1", [3, 6, 7], 0.05)

#p1 = Player(1)
#p1 = EndStatePlayer(1, net11)
#p1 = MonteCarloPlayer(1, net12, 10)
p1 = QLearningPlayer(1, net13, 0.1, 0.9)

#net21 = Network("Endstate2", [3, 6, 7], 0.01)
#net22 = Network("MonteCarlo2", [3, 6, 7], 0.01)
net23 = Network("Qlearning2", [3, 6, 7], 0.05)

#p2 = Player(2)
#p2 = EndStatePlayer(2, net21)
#p2 = MonteCarloPlayer(2, net22, 10)
p2 = QLearningPlayer(2, net23, 0.2, 0.9)

#board = np.zeros((6, 7), dtype=np.int8)
g = Game(p1, p2)#, board)


'''
    MAIN TRAINING LOOP
'''


start = time.time()

epochs = 20 #25
tra_iterations = 400 #1000
val_iterations = 100

for i in range(epochs):   

    # Adjust exploration chance
    explore_rate = max(0.1, 1.0-(0.1*i))
    p1.explore_rate=explore_rate
    p2.explore_rate=explore_rate

    # Training cycle
    for _ in tqdm(range(tra_iterations)):

        winner = g.play_game(True)
    
        #printGame(g.board, winner)
        
        if (winner == 0):
            p1.tell_outcome(g.board, 0.5)
            p2.tell_outcome(g.board, 0.5)
        elif (winner == p1.value):
            p1.tell_outcome(g.board, 1.0)
            p2.tell_outcome(g.board, 0.0)
        else:
            p1.tell_outcome(g.board, 0.0)
            p2.tell_outcome(g.board, 1.0)
    
        g.reset_board()
        g.switch_players()
        
    # Validation cycle
    wins_p1 = 0.0
    wins_p2 = 0.0
    draws = 0.0
    test_game = Game(p1, Player(2))#, board) #Game(p1, Player(2), board)
    for j in tqdm(range(val_iterations)):
        winner = test_game.play_game(False)
        
        if (winner == p1.value):
            wins_p1 += 1.0

        if (winner == p2.value):
            wins_p2 += 1.0
            
        elif (winner == 0):
            draws += 1.0
        if j < 5:
            test_game.print_board()
        test_game.reset_board()
        test_game.switch_players()
            
    print "Epoch {0}:".format(i+1)
    print "Win percentage P1: {0}".format(wins_p1/(val_iterations))
    print "Win percentage P2: {0}".format(wins_p2/(val_iterations))
    print "Draw percentage: {0}".format(draws/(val_iterations))

    
print "Done!"
print str(time.time() - start) + " seconds"

