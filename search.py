# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 14:42:46 2017

@author: alcaz
"""
# Create the data structure for the frontier
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
    


    
class node(object):
    '''
    This class is the data structure to keep track of the search tree.
    '''
    def __init__(self, state, parent = None, action = None, path_cost = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        
    def get_state(self):
        return self.state
    
    def get_parent(self):
        return self.parent
        

# how to obtain the child of a given node? That's depends of the result of the
# action, and this depends of the problem formulation... so it's neccessary
# to program a function that use the problem formulation class and also
# the node class to create the respective child


def child_node(problem, parent, action):
    '''
    problem: the object with the problem formulation
    parent: the parent node to obtain the child
    action: the action applied to the parent node
    Return the child node generated by  by the result of the action applied to 
        the parent node
    '''
    state = problem.result(parent.state, action)
    update_cost = parent.path_cost + problem.step_cost(parent.state, action)
    child = node(state, parent = parent, action = action, path_cost = update_cost)
    return child
    





        
        

