import copy
import math

# setting
# H(m,n,k)
m = 20
n = 20
k = 0

# measure length of permutation group.
if k != 0 :
    lenlist = m + n - 2
else:
    lenlist = m + n - 1

# Define goal of the permutation.
goal = []
for element in list(range(lenlist)):
    goal.append(element+1)

#=============================================================================
# Create node represent the states of Hungarian rings.
class Node():
    # status is the permutation of hungarian ring in this step.
    def __init__(self, status, lastMove, repMove, parent, cost):
        self.status = status
        self.lastMove = lastMove
        self.repMove = repMove
        self.parent = parent
        self.cost = cost


#=============================================================================
# List of all action that we can use.
# 'LCW' is rotating left ring clocklwise 1 time.
# 'LCC' is rotating left ring counter-cloclwise 1 time.
# 'RCW' is rotating right ring clocklwise 1 time.
# 'RCC' is rotating right ring counter-cloclwise 1 time.        
actionList = ['LCW', 'LCC', 'RCW', 'RCC']


#=============================================================================
# Define each action to swap position of elements on a state,
# Then return the child node after swap position.
def transition(node, action):
    statusBf = copy.deepcopy(node.status)
    statusAf = copy.deepcopy(node.status)
    cost = node.cost
    
    if action == 'LCW': #ring m
        for i in range(m):
            if i != m-1 :
                statusAf[i+1] = statusBf[i]
            else:
                statusAf[0] = statusBf[i]
        
        if node.lastMove == 'LCW':
            repMove = node.repMove + 1
            if repMove == m:
                statusAf = None    
        else:
            repMove = 1  

    if action == 'LCC': #ring m
        for i in range(m):
            if i != m-1 :
                statusAf[i] = statusBf[i+1]
            else:
                statusAf[i] = statusBf[0]
        
        if node.lastMove == 'LCC':
            repMove = node.repMove + 1
            if repMove == m:
                statusAf = None    
        else:
            repMove = 1  

    if action == 'RCW': #ring n
        for i in range(n):
            if i < n-2 :
                statusAf[m+i+1] = statusBf[m+i]
            elif i == n -2 :
                statusAf[0] = statusBf[m+i]
            elif i == n-1 :
                statusAf[m] = statusBf[0]
        
        if node.lastMove == 'RCW':
            repMove = node.repMove + 1
            if repMove == n:
                statusAf = None    
        else:
            repMove = 1          

    if action == 'RCC': #ring n
        for i in range(n):
            if i < n-2 :
                statusAf[m+i] = statusBf[m+i+1]
            elif i == n -2 :
                statusAf[m+i] = statusBf[0]
            elif i == n-1 :
                statusAf[0] = statusBf[m]
        
        if node.lastMove == 'RCC':
            repMove = node.repMove + 1
            if repMove == n:
                statusAf = None    
        else:
            repMove = 1

    child = Node(statusAf, action, repMove, node, cost+1)
    if statusAf == None :
        return(None)
    else:
        return(child)

#=============================================================================
# Recive a node then do each action to that node 
# and return all of its child nodes.
def expand(node):
    listNextNode = []
    for action in actionList:
        child = transition(node, action)
        if child != None:
            listNextNode.append(child)
    return(listNextNode)

#=============================================================================
# Recive a node then check is it goal or not.
def goalCheck(node):
    if node.status == goal:
        return(True)
    else:
        return(False)

#=============================================================================
# Recive the initial node then expand node until get goal node.
# Return the list of nodes that lead to goal node.
def solve(initial):    
    frontier = [initial]
    solution = []
    visited = []
    while True:
        if len(frontier) == 0:
            break
        else:
            node = frontier.pop(0) #HERE!!!!!!!!!!!!!!
            if goalCheck(node):
                path = [node]
                while node.parent != None : 
                    path.insert(0, node.parent)
                    node = node.parent                
                solution = path
                break
            else:
                for item in expand(node):
                    repeat = False
                    for oldNode in visited:
                        if oldNode.status == item.status :
                            repeat = True
                            break
                    if not repeat:
                        visited.append(item)
                        frontier.append(item)
                print(len(visited))                      
    return(solution)

#=============================================================================
# Recieve list of nodes then print last move and state for each node.
def printSolution(solution):
    for node in solution:
        print(node.lastMove,node.status)

#=============================================================================
#=============================================================================

initial = Node([37, 1, 2, 32, 4, 33, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                17, 36, 19, 18, 38, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                30, 31, 3, 34, 5, 35], None, None, None,0)
sln = solve(initial)
printSolution(sln)