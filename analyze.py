from Game import *
from MDP_Solver import *
from QLearning import *

def analyze_methods():
    i = 1
    n = 2 #number of grids

    LVL = "EASY"

    filename = "analyse_"+LVL


    while (i <= n) :
        G = Game.random_generation(10*i, 10*i, LVL)

        if not G.is_winnable() :
            continue

        ####--------------------- ITV
        # t1 = time.time()
        # policy = G.mdp.run_value_iteration(0.01)
        # t2 = time.time() - t1
        # nb_mouvement = G.play_with_policy(policy,False)
        #
        # f = open(filename+"_ITV","a")
        # f.write(str(nb_mouvement)+" "+str(t2)+" "+str(i*10)+" "+str(i*10)+"\n")
        # f.close()

        ####--------------------- LP
        # Game = new Game(".game")
        # t1 = time.time()
        # policy = G.mdp.run_linear_programming_resolution()
        # t2 = time.time() - t1
        # nb_mouvement = G.play_with_policy(policy,False)
        # f = open(filename+"_LP","a")
        # f.write(str(nb_mouvement)+" "+str(t2)+" "+str(i*10)+" "+str(i*10)+"\n")
        # f.close()

        ####--------------------- QL
        QL = QLearning(".game")

        t1 = time.time()
        policy = QL.run_Q_learning()
        t2 = time.time() - t1
        G = Game(".game")
        nb_mouvement = G.play_with_policy(policy,False)

        f = open(filename+"_QL","a")
        f.write(str(nb_mouvement)+" "+str(t2)+" "+str(i*10)+" "+str(i*10)+"\n")
        f.close()

        i += 1


analyze_methods()