import multiprocessing
import copy

class Node:
    def __init__(self, gamestate):
        self.state = gamestate
        self.children = []
    
    def addChild(self, child):
        self.children.append(child)

    def getChildren(self):
        return self.children

    def __str__(self):
        return str(self.state) + " " + str(len(self.children))

def buildBaseState(edgeSize):
    baseState = []
    row = []
    for i in range(edgeSize):
        row.append(0)
    for i in range(edgeSize):
        baseState.append(row.copy())
    return baseState

def multiprocessedTree(n):
    state = buildBaseState(n)
    processes = []

    resultQueue = multiprocessing.Queue()

    for i in range(len(state)):
        for j in range(len(state[i])):
            posState = copy.deepcopy(state)
            posState[i][j] = 1
            processes.append(multiprocessing.Process(target=parallel_funct, args=(posState, resultQueue)))
            negState = copy.deepcopy(state)
            negState[i][j] = -1
            processes.append(multiprocessing.Process(target=parallel_funct, args=(negState, resultQueue)))
    for i, process in enumerate(processes):
        print("starting thread " + str(i+1) + "...")
        process.start()
    for i, process in enumerate(processes):
        process.join()
        #TODO: why do some threads not end?

    rootNode = Node(state)
    # add all subtrees to root node
    while not resultQueue.empty():
        rootNode.addChild(resultQueue.get())
    return rootNode

def parallel_funct(state, rootNodeChildren):
    print("generating subtree from state " + str(state))
    rootNodeChildren.put(createNode(state)) 

def createNode(state):
    newNode = Node(state)
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 0:
                nodeOne = copy.deepcopy(state)
                nodeOne[i][j]= 1
                oneNode = createNode(nodeOne)
                nodeNegOne = copy.deepcopy(state)
                nodeNegOne[i][j]= -1
                negOneNode = createNode(nodeNegOne)
                if oneNode != None:
                    newNode.addChild(oneNode)
                if negOneNode != None:
                    newNode.addChild(negOneNode)
    print(newNode.state, str(len(newNode.children)) + " children")
    return newNode

n = 2
if __name__ == '__main__':
    # threading is still a WIP
    # multiprocessedTree(n)
    createNode(buildBaseState(n))