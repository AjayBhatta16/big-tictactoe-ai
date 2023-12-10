import multiprocessing
import copy
from square_matrix import SquareMatrix

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
    return False

def create_node(state, isBotTurn):
    newNode = Node(state)
    for i in range(state.get_size()):
        for j in range(state.get_size()):
            if state.get_value(i, j) == 0:
                nodeOne = copy.deepcopy(state)
                if isBotTurn:
                    nodeOne.set_value(i, j, 1)
                else:
                    nodeOne.set_value(i, j, -1)
                if not has_win_state(newNode.state):
                    oneNode = create_node(nodeOne, not isBotTurn)
                if oneNode != None:
                    newNode.add_child(oneNode)
    # print(newNode.state, str(len(newNode.children)) + " children")
    return newNode

# I wouldn't reccomend running n>3 on your own machine
n = 3
if __name__ == '__main__':
    nodes = multiprocessed_tree(n)
    print(str(nodes.get_total_nodes()) + " total nodes")
    #createNode(buildBaseState(n))