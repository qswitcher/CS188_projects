# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]


class Node:
    """
    Search node used in graph search
    """
    def __init__(self, state, actions=[], totalCost=0):
        self.state = state
        self.actions = actions
        self.totalCost = totalCost  # total path cost

    def branch(self, successor, action, stepCost):
        new_actions = list(self.actions)
        new_actions.append(action)
        return Node(successor, 
                    new_actions,
                    self.totalCost + stepCost)


class GraphSearch:
    """
    Generalized graph search. 
    """
    def __init__(self, queue_class, *queue_args):
        self.queue_class = queue_class
        self.queue_args = queue_args

    def search(self, problem):
        closed = set()
        fringe = self.queue_class(*self.queue_args)
        fringe.push(Node(problem.getStartState()))
        while True:
            if fringe.isEmpty():
                return False
            node = fringe.pop()
            if problem.isGoalState(node.state):
                return node.actions
            if node.state not in closed:
                closed.add(node.state)
                for successor_args in problem.getSuccessors(node.state):
                    fringe.push(node.branch(*successor_args))



def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    graph_search = GraphSearch(util.Stack)
    return graph_search.search(problem)

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    graph_search = GraphSearch(util.Queue)
    return graph_search.search(problem)

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    def priority_fun(node):
        return node.totalCost

    graph_search = GraphSearch(util.PriorityQueueWithFunction, priority_fun)
    return graph_search.search(problem)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    def priority_fun(node):
        return heuristic(node.state, problem) + node.totalCost

    graph_search = GraphSearch(util.PriorityQueueWithFunction, priority_fun)
    return graph_search.search(problem)    


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
