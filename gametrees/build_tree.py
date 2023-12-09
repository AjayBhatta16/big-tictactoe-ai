import multiprocessing
import copy

class Node:
    def __init__(self, gamestate):
        self.state = gamestate
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children

    def __str__(self):
        return str(self.state) + " " + str(len(self.children))

def build_base_state(edgeSize):
    baseState = []
    row = []
    for i in range(edgeSize):
        row.append(0)
    for i in range(edgeSize):
        baseState.append(row.copy())
    return baseState

def multiprocessed_tree(n):
    state = build_base_state(n)
    processes = []

    resultQueue = multiprocessing.Queue()

    for i in range(len(state)):
        for j in range(len(state[i])):
            # these states will never appear in gameplay, as the bot never goes first
            # posState = copy.deepcopy(state)
            # posState[i][j] = 1
            # processes.append(multiprocessing.Process(target=parallel_funct, args=(posState, resultQueue)))
            negState = copy.deepcopy(state)
            negState[i][j] = -1
            processes.append(multiprocessing.Process(target=parallel_funct, args=(negState, resultQueue)))
    
    # start threads
    for i, process in enumerate(processes):
        print("starting thread " + str(i+1) + "...")
        process.start()

    # append results from each thread as they are generated
    results = [resultQueue.get() for process in processes]

    # ensure function doesn't return before all threads are complete
    for i, process in enumerate(processes):
        process.join()

    rootNode = Node(state)

    # add all subtrees to root node
    for result in results:
        rootNode.add_child(result)
    return rootNode

def parallel_funct(state, rootNodeChildren):
    print("generating subtree from state " + str(state))
    rootNodeChildren.put(create_node(state))

def create_node(state):
    newNode = Node(state)
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 0:
                nodeOne = copy.deepcopy(state)
                nodeOne[i][j]= 1
                oneNode = create_node(nodeOne)
                nodeNegOne = copy.deepcopy(state)
                nodeNegOne[i][j]= -1
                negOneNode = create_node(nodeNegOne)
                if oneNode != None:
                    newNode.add_child(oneNode)
                if negOneNode != None:
                    newNode.add_child(negOneNode)
    #print(newNode.state, str(len(newNode.children)) + " children")
    return newNode

# I wouldn't reccomend running n>2 on your own machine
n = 2
if __name__ == '__main__':
    nodes = multiprocessed_tree(n)
    #createNode(buildBaseState(n))