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
      
    def __str__(self):
        result = ''
        for e in self.list:
            result = result + str(e) + ', '
        return '<' + result[:-2] + '>'
   


class stack(queue):
    '''
    Implementation of a stack list (LIFO queue) based on queue class.
    Rewrite the insert and pop method of the queue class (FIFO).
    '''
    def __init__(self, elements):
        queue.__init__(self, elements)
    
    def insert(self, element):
        '''
        Insert an element in the queue list and return the queue list.
        '''
        self.list = [element] + self.list
        return self.list
    
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
        self.state = puzzle
        self.goal = goal
        self.puzzle_length = len(puzzle)
        self.board_size = int(len(puzzle) ** 0.5)
        
    def get_state(self):
        '''
        Return the tuple representation of the puzzle.
        '''
        return self.state[:]
        
    def set_state(self, puzzle):
        '''
        Change the state values with a new puzzle configuration.
        '''
        self.state = puzzle
        
    def show_board(self):
        '''
        For visualize the board of the puzzle in a matrix way, each row in a row.
        '''
        self.board = []
        for j in range(0, self.puzzle_length, self.board_size):
            self.board.append(list(self.state[j:(j + self.board_size)]))
        for i in range(len(self.board)):
            print(self.board[i], sep = '\n')
            
    def actions(self):
        '''
        Get the movements of the blank space (actions) with the following convention
        order: 'Up', 'Down', 'Left' and 'Right'. Different subsets of these are
        possible dependeding (available movements) on where the blank space is.
        
        Return a tuple with all the available movements from the board instance
            blank space.
        '''
        self.movements = ()
        # find the blank space index
        self.blank_space = self.state.index(0)
        # define the constraint indexes for movements
        self.up_cons = self.state[:self.board_size]
        self.down_cons = self.state[self.puzzle_length - \
                                        self.board_size:self.puzzle_length]
        self.left_cons = self.state[::self.board_size]
        self.right_cons = self.state[self.board_size - 1::self.board_size]
        if 0 not in self.up_cons:
            # a 'Up' movement available
            self.movements += ('Up',)
        if 0 not in self.down_cons:
            # a 'Down' movement available
            self.movements += ('Down',)
        if 0 not in self.left_cons:
            # a 'Left' movement available
            self.movements += ('Left',)
        if 0 not in self.right_cons:
            # a 'Right' movement available
            self.movements += ('Right',)
        return self.movements
        
    def result(self, movement):
        '''
        Apply a given movement to the current puzzle.
        
        Return a tuple with the configuration of a new puzzle resulting from
            applied the given movement to the current puzzle.
        '''
        # find the blank space index
        self.blank_space = self.state.index(0)
        # create a copy from the current state
        self.new_state = list(self.get_state())
        # execute the corresponding movement swap
        if movement == 'Up':
            self.swap_value = self.new_state[self.blank_space - self.board_size]
            self.new_state[self.blank_space - self.board_size] = 0
        if movement == 'Down':
            self.swap_value = self.new_state[self.blank_space + self.board_size]
            self.new_state[self.blank_space + self.board_size] = 0
        if movement == 'Left':
            self.swap_value = self.new_state[self.blank_space - 1]
            self.new_state[self.blank_space - 1] = 0
        if movement == 'Right':
            self.swap_value = self.new_state[self.blank_space + 1]
            self.new_state[self.blank_space + 1] = 0
        self.new_state[self.blank_space] = self.swap_value
        return tuple(self.new_state)  
    
    def goal_test(self, state):
        '''
        Determine whether a given state is a goal state
        '''
        return self.state == self.goal
    
    def step_cost(self):
        '''
        The step cost of taking an action to generate a node. For now a constant.
        '''
        return 1



x = [y for y in range(9)]
x = problem(x)           
x.get_state()
x.show_board()
x.step_cost()


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
        child_state = problem.result(action)
        update_cost = self.path_cost + problem.step_cost()
        child = node(child_state, parent = self, action = action, path_cost = update_cost)
        return child
    
    def expand(self, problem, reverse = False):
        '''
        Return a list of the child nodes of the node.
        '''
        return [self.child_node(problem, action) for action in problem.actions()]
    
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
        
        
    
    
        

nodo1 = problem((7, 3, 1, 8, 2, 4, 5, 6, 0))
nodo1.show_board()
nodo1.actions()
nodo1.result('Up')

x = node(nodo1.state)
x.parent
x.state
x.depth
x.path_cost
x.child_node(nodo1, 'Up').state
x.expand(nodo1)

y = x.expand(nodo1)[0]
z = y.expand(nodo1)[0]
z.solution()
x.state
y.state
z.state

    


        
        
        
    



        
        

