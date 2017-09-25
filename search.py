# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 14:42:46 2017

@author: Cristobal Alcazar
"""
# =============================================================================
#                         Frontier Data Structures
# =============================================================================
class queue(object):
    '''
    Implementation of a queue list (FIFO) based on the built-in class list.
    The newest elements are inserted in the first positions. So the oldest
    ones are in the tail of the list.
    '''
    def __init__(self, elements):
        self.list = elements
    
    def insert(self, element):
        '''
        Insert an element in the queue list and return the queue list.
        '''
        self.list = [element] + self.list
        return self.list
    
    def pop(self):
        '''
        Remove the oldest element of the queue and returns it.
        '''
        return self.list.pop()
    
    def empty(self):
        '''
        Return True if the queue is empty.
            Otherwise, return False.
        '''
        return len(self.list) == 0
    
    def __iter__(self):
        '''
        Make the queue list an iterable object.
        '''
        return iter(self.list)
    
    def member(self, other):
        members = set(self.list)
        return other == members
      
    def __str__(self):
        result = ''
        for e in self.list:
            result = result + str(e) + ', '
        return '<' + result[:-2] + '>'
   


class stack(queue):
    '''
    Implementation of a stack list (LIFO queue) based on queue class.
    Rewrite the pop method of the queue class (FIFO).
    '''
    def __init__(self, elements):
        queue.__init__(self, elements)
    
    
    def pop(self):
        '''
        Remove the newest element of the queue and returns it.
        '''
        return self.list.pop(0)
    

    
# =============================================================================
#                            Problem Formulation
# =============================================================================
class problem(object):
    '''
    This class represent the low-level physical configuration of the board. The
    tiles plus the blank space that conformed the puzzle game. In other words,
    is the formulation of the specific problem: 8 - puzzles
    '''
    def __init__(self, puzzle, goal = (0, 1, 2, 3, 4, 5, 6, 7, 8)):
        '''
        Initializes a puzzle represented as a tuple.
        puzzle introduce the puzzle's values in row-wise order from the first 
        row to the last.
        Warning: This class work only with square puzzles, i.e. n x n boards.
        '''
        self.initial_state = puzzle
        self.goal = goal
        self.puzzle_length = len(puzzle)
        self.board_size = int(len(puzzle) ** 0.5)
        
        
    def show_board(self, state):
        '''
        For visualize the board of the puzzle in a matrix way, each row in a row.
        '''
        board = []
        for j in range(0, self.puzzle_length, self.board_size):
            board.append(list(state[j:(j + self.board_size)]))
        for i in range(len(board)):
            print(board[i], sep = '\n')
            
    def actions(self, state):
        '''
        Get the movements of the blank space (actions) with the following convention
        order: 'Up', 'Down', 'Left' and 'Right'. Different subsets of these are
        possible dependeding (available movements) on where the blank space is.
        
        Return a list with all the available movements from the board instance
            blank space.
        '''
        movements = []
        # define the constraint indexes for movements
        up_cons = state[:self.board_size]
        down_cons = state[self.puzzle_length - \
                                        self.board_size:self.puzzle_length]
        left_cons = state[::self.board_size]
        right_cons = state[self.board_size - 1::self.board_size]
        if 0 not in up_cons:
            # a 'Up' movement available
            movements += ('Up',)
        if 0 not in down_cons:
            # a 'Down' movement available
            movements += ('Down',)
        if 0 not in left_cons:
            # a 'Left' movement available
            movements += ('Left',)
        if 0 not in right_cons:
            # a 'Right' movement available
            movements += ('Right',)
        return movements
        
    def result(self, state, action):
        '''
        Apply a given movement to the current puzzle.
        
        Return a tuple with the configuration of a new puzzle resulting from
            applied the given movement to the current puzzle.
        '''
        state = list(state)
        # find the blank space index
        blank_space = state.index(0)
        # create a copy from the current state
        new_state = state[:]
        # execute the corresponding movement swap
        if action == 'Up':
            swap_value = new_state[blank_space - self.board_size]
            new_state[blank_space - self.board_size] = 0
        if action == 'Down':
            swap_value = new_state[blank_space + self.board_size]
            new_state[blank_space + self.board_size] = 0
        if action == 'Left':
            swap_value = new_state[blank_space - 1]
            new_state[blank_space - 1] = 0
        if action == 'Right':
            swap_value = new_state[blank_space + 1]
            new_state[blank_space + 1] = 0
        new_state[blank_space] = swap_value
        return tuple(new_state)  
    
    def goal_test(self, state):
        '''
        Determine whether a given state is a goal state
        '''
        return state == self.goal
    
    def step_cost(self):
        '''
        The step cost of taking an action to generate a node. For now a constant.
        '''
        return 1




# =============================================================================
#                            Graph Data Structures
# =============================================================================
class node(object):
    '''
    This class is the data structure to keep track the search in the the tree.
     state: the state in the state space to which the node corresponds.
     parent: the NODE (object) in the search tree that generated this node.
     action: the action that was applied to the parent to generate the node.
     path_cost: the cost, denoted by g(n), of the path from the initial 
            state to the node, as indicated by the parent pointers.
    depth: 
    '''
    def __init__(self, state, parent = None, action = None, path_cost = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1
        
    def child_node(self, problem, action):
        '''
        Generate the child node of the current node given a valid action.
        '''
        child_state = problem.result(self.state, action)
        update_cost = self.path_cost + problem.step_cost()
        child = node(child_state, parent = self, action = action, path_cost = update_cost)
        return child
    
    def expand(self, problem, reverse = False):
        '''
        Return a list of the child nodes of the node.
        '''
        if reverse == True:
            available_actions = problem.actions(self.state)
            available_actions.reverse()
            return [self.child_node(problem, action) for action in available_actions]
        return [self.child_node(problem, action) for action in problem.actions(self.state)]
    
    def path(self):
        '''
        Return a list of nodes forming the path from the root to this node.
        '''
        node, path_nodes = self, []
        while node:
            path_nodes.append(node)
            node = node.parent
        return list(reversed(path_nodes))
    
    def solution(self):
        '''
        Return the sequence of actions obtained by following the parent pointers
        back to the root. Using the list of nodes output of the method path.
        '''
        return [node.action for node in self.path()[1:]]
    
    def __eq__(self, other):
        return isinstance(other, node) and self.state == other.state
        
        
    
x = problem((0, 1, 2, 3, 4, 5, 6, 7, 8))
nod1 = node((0, 1, 2, 3, 4, 5, 6, 7,8))        
nod2 = node((8, 1, 2, 3, 4 ,5, 6, 7, 0))
nod3 = node((0, 1, 2, 3, 4, 5, 6, 8, 7))
nod1 == nod2
f = [nod1, nod2]
nod1 in f
nod3 in f

d = x.actions(nod1.state)
d.reverse()
d
x.actions(nod1.state)

x = [1, 2, 3]
[elem for elem in x.reverse]

x.reverse()
x
x    
# =============================================================================
#                              Uninformed Search
# =============================================================================

# create a format function for the output
def output(node):
    '''
    Create the output file with the given format.
    '''
    pass



# Breadth-First Search algorithm
def bfs(problem):
    '''
    Breadth-first-search algorithm.
    Return a solution, or failure
    '''
    import time
    start_time = time.clock()
    root_node = node(problem.initial_state)
    # initialize the frontier with an empty queue list
    frontier = queue([])
    frontier.insert(root_node)
    explored = set()
    nodes_expanded = 0
    while frontier:
        current_node = frontier.pop()
        explored.add(str(current_node.state))
        if problem.goal_test(current_node.state):
            # use the output function over the node with the solution to 
            # obtain the following observations...
            path = current_node.solution()
            cost_path = current_node.path_cost
            depth = current_node.depth
            max_depth = frontier.list[0].depth
            running_time = round(time.clock() - start_time, 8)
            print('\npath_to_goal: ', path,
                  '\ncost_of_path: ', cost_path,
                  '\nnodes_expanded: ', nodes_expanded,
                  '\nsearch_depth: ', depth,
                  '\nmax_search_depth: ', max_depth,
                  '\nrunning_time: ', running_time)
            return True
        nodes_expanded += 1
        for child in current_node.expand(problem):
            if str(child.state) not in explored and child not in frontier:
                frontier.insert(child)
    return False


test = problem((1,2,5,3,4,0,6,7,8))
bfs(test)


def dfs(problem):
    '''
    Depth-First-Search algorithm.
    Return a solution, or failure
    '''
    import time
    start_time = time.clock()
    root_node = node(problem.initial_state)
    frontier = stack([])
    frontier.insert(root_node)
    explored = set()
    nodes_expanded = 0
    while frontier:
        current_node = frontier.pop()
        explored.add(str(current_node.state))
        if problem.goal_test(current_node.state):
            path = current_node.solution()
            cost_path = current_node.path_cost
            depth = current_node.depth
            max_depth = frontier.list[0].depth
            running_time = round(time.clock() - start_time, 8)
            print('\npath_to_goal: ', path,
                  '\ncost_of_path: ', cost_path,
                  '\nnodes_expanded: ', nodes_expanded,
                  '\nsearch_depth: ', depth,
                  '\nmax_search_depth: ', max_depth,
                  '\nrunning_time: ', running_time)
            return True
        nodes_expanded += 1
        for child in current_node.expand(problem, reverse = True):
            if str(child.state) not in explored and frontier.member(child):
                frontier.insert(child)
    return False

# arreglar problemas con dfs
# ver como checkear nuevas nodos generados en la lista de la frontera
# en complejidad O(1)
test = problem((1,2,5,3,4,0,6,7,8))
dfs(test)


x = [1, 2, 3]   
y = stack(x)    
z = queue(x) 
y.pop()
z.pop()
