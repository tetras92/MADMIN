import random
from Action import Action



def generate_position_cells_t(n,m,prop_cells_type):

    L = [ list() for i in range(n)]

    for i in range(n) :
        L[i] = [ "B" for j in range(m)]
        
    coordonnees = [ (i,j) for j in range(m) for i in range(n)  if not(i==0 and j==0) and not(i==n-1 and j==m-1) ]
    for t_cell,nb_t in prop_cells_type.items():
        if((t_cell != 'T')) :
            cpt = nb_t
            while(cpt > 0):
                l,c = coordonnees.pop( random.randint(0,len(coordonnees) - 1) )
                L[l][c] = t_cell
                cpt -= 1

    L[0][0] = "T"
    # L[n-1][m-1] = "B"
    
    return L    
    

    

def generate_file_game(L):
    n = len(L)
    m = len(L[0])
    f = open(".game", "w")
    f.write(str(n)+" "+str(m)+"\n")
    
    for i in range(n):
        line = ""
        for j in range(m):
            line += L[i][j]+ " "
        f.write(line+"\n")
    
    f.close()


def print_policy(policy, X, Y):
        xS = [ [ None for j in range(Y)] for i in range(X) ]
        xK = [ [ None for j in range(Y)] for i in range(X) ]
        xSK = [ [ None for j in range(Y)] for i in range(X) ]
        xKT = [ [ None for j in range(Y)] for i in range(X) ]
        xSKT = [ [ None for j in range(Y)] for i in range(X) ]
        xNone = [ [ None for j in range(Y)] for i in range(X) ]

        for state,action in policy.items():
            (i,j),S,K,T = state
            if S :
                if not K:
                    xS[i][j] = action
                elif K :
                    if not T :
                        xSK[i][j] = action
                    else :
                        xSKT[i][j] = action
            elif K :
                if not T:
                    xK[i][j] = action
                else :
                    xKT[i][j] = action
            else :
                xNone[i][j] = action

        def printing(x):
            line = ""
            s = ""
            for i in range(len(x)) :
                s += "\n | "
                for j in range(len(x[i])) :
                    if x[i][j] == Action.RIGHT :
                        s += ">"
                    elif x[i][j] == Action.LEFT :
                        s += "<"
                    elif x[i][j] == Action.UP :
                        s += "^"
                    else :
                        s += "v"
                    s += " | "
            print(s)

        print(" \n ********* Policy when nothing : *********")
        printing(xNone)
        print(" \n ********* Policy when S : *********")
        printing(xS)
        print(" \n ********* Policy when K : *********")
        printing(xK)
        print(" \n ********* Policy when SK : *********")
        printing(xSK)
        print(" \n ********* Policy when KT : *********")
        printing(xKT)
        print(" \n ********* Policy when SKT : *********")
        printing(xSKT)
