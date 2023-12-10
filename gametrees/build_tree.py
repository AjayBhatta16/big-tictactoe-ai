import multiprocessing
import copy
from square_matrix import SquareMatrix
import math

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
    
    def get_total_nodes(self):
        totalNodes = 0
        for child in self.children:
            totalNodes += child.get_total_nodes()
        return totalNodes + 1

def build_base_state(edgeSize):
    return SquareMatrix(edgeSize)

def multiprocessed_tree(n):
    state = build_base_state(n)
    processes = []

    resultQueue = multiprocessing.Queue()

    for i in range(state.get_size()):
        for j in range(state.get_size()):
            negState = copy.deepcopy(state)
            # -1 user always goes first
            negState.set_value(i, j, -1)
            processes.append(multiprocessing.Process(target=parallel_funct, args=(negState, resultQueue)))
    
    # start processes
    for i, process in enumerate(processes):
        print("starting process " + str(i+1) + "...")
        process.start()

    # append results from each process as they are generated
    results = [resultQueue.get() for process in processes]

    # ensure function doesn't return before all processes are complete
    for i, process in enumerate(processes):
        process.join()

    rootNode = Node(state)

    # add all subtrees to root node
    for result in results:
        rootNode.add_child(result)
    return rootNode

def parallel_funct(state, rootNodeChildren):
    print("generating subtree from state " + str(state))
    rootNodeChildren.put(create_node(state, True))

#TODO: would help performance
def has_win_state(state):
    win_len = min(state.get_size(), 4)
    win_shift = win_len-1
    # check rows
    for i in range(state.get_size()):
        for j in range(state.get_size()-win_shift):
            total = 0
            for x in range(win_len):
                total += state.get_value(i, j+x)
            if abs(total) == win_len:
                return True
    # check columns
    for i in range(state.get_size()-win_shift):
        for j in range(state.get_size()):
            total = 0
            for x in range(win_len):
                total += state.get_value(i+x, j)
            if abs(total) == win_len:
                return True
    # check diagonal TL to BR
    for i in range(state.get_size()-win_shift):
        for j in range(state.get_size()-win_shift):
            total = 0
            for x in range(win_len):
                total += state.get_value(i+x, j+x)
            if abs(total) == win_len:
                return True
    # check diagonal TR to BL
    for i in range(state.get_size()-win_shift):
        for j in range(win_shift, state.get_size()):
            total = 0
            for x in range(win_len):
                total += state.get_value(i+x, j-x)
            if abs(total) == win_len:
                return True
    # no  winner
    return False

def create_node(state, isBotTurn):
    newNode = Node(state)
    if has_win_state(state):
        var = 1
        # print(str(state) + " - winstate, ignoring")
    else:
        for i in range(state.get_size()):
            for j in range(state.get_size()):
                # create child nodes where there's an empty spot and append to current node
                if state.get_value(i, j) == 0:
                    potentChildState = copy.deepcopy(state)
                    if isBotTurn:
                        potentChildState.set_value(i, j, 1)
                    else:
                        potentChildState.set_value(i, j, -1)
                    newNodeChild = create_node(potentChildState, not isBotTurn)
                    newNode.add_child(newNodeChild)
                    # print(newNode.state, str(len(newNode.children)) + " children")
    return newNode

# I wouldn't reccomend running n>3 on your own machine
n = 3
if __name__ == '__main__':
    nodes = multiprocessed_tree(n)
    print(str(nodes.get_total_nodes()) + " total nodes")
    #createNode(buildBaseState(n))