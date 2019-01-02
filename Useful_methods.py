import random

#
# def read_nb_cells_type(filename):
#     prop = dict()
#     f = open(filename,"r")
#     for line in f:
#         prop[str(line[0])] = int(line[2])
#     return prop



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
