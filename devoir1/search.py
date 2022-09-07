from __future__ import annotations
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from typing import Any, List, Literal, Optional
from game import Directions
from dataclasses import dataclass

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """util.raiseNotDefined()
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

Direction = Literal['NORTH', 'SOUTH', 'EAST', 'WEST', 'STOP']

@dataclass(eq=False)
class Node:
    state: Any
    previous: Optional[Node] = None
    direction: Optional[Direction] = None

    @property
    def path(self: Node) -> List[Direction]:
        if self.previous is None:
            return []
        return self.previous.path + [self.direction]

    def __eq__(self, __o: Node) -> bool:
        return self.state == __o.state

    def __hash__(self) -> int:
        return hash(self.state)

@dataclass(eq=False)
class PNode(Node):
    """
    Node used for A* and UCS
    """
    previous: Optional[PNode] = None # overwrite
    cost: int = 0 # Cost from the start


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    """
    visited = set() # visited nodes
    stack = util.Stack()
    stack.push(Node(problem.getStartState()))

    while not (stack.isEmpty() or problem.isGoalState((node := stack.pop()).state)):
        if node in visited:
            continue
        visited.add(node)
        for state, direction, _, in problem.getSuccessors(node.state):
            stack.push(Node(state, node, direction))

    return node.path if problem.isGoalState(node.state) else []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    visited = set() # visited nodes
    q = util.Queue()
    q.push(Node(problem.getStartState()))

    while not (q.isEmpty() or problem.isGoalState((node := q.pop()).state)):
        if node in visited:
            continue
        visited.add(node)
        for state, direction, _, in problem.getSuccessors(node.state):
            q.push(Node(state, node, direction))

    return node.path if problem.isGoalState(node.state) else []
        
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    
    visited = set()
    queue = util.PriorityQueue()
    queue.push(PNode(problem.getStartState()), 0)

    while not (queue.isEmpty() or problem.isGoalState((node := queue.pop()).state)):
        if node in visited:
            continue
        visited.add(node)
        for state, direction, cost in problem.getSuccessors(node.state):
            next_node = PNode(state, node, direction, node.cost + cost)
            queue.push(next_node, next_node.cost)

    return node.path if problem.isGoalState(node.state) else []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    visited = set()
    queue = util.PriorityQueue()
    queue.push(PNode(problem.getStartState()), heuristic(problem.getStartState(), problem))

    while not (queue.isEmpty() or problem.isGoalState((node := queue.pop()).state)):
        if node in visited:
            continue
        visited.add(node)
        for state, direction, cost in problem.getSuccessors(node.state):
            next_node = PNode(state, node, direction, node.cost + cost)
            queue.push(next_node, next_node.cost + heuristic(state, problem))
    
    return node.path if problem.isGoalState(node.state) else []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
