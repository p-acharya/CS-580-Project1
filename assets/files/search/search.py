# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC
# Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't
    implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


class SearchNode:
    def __init__(self, position, parent=None, action=None, path_cost=0):
        self.position = position
        self.parent = parent
        self.action = action
        self.path_cost = path_cost


def generic_search(problem, fringe):
    start_node = SearchNode(position=problem.getStartState())
    fringe.push(start_node)
    visited = set()

    while not fringe.isEmpty():
        current_node = fringe.pop()

        if problem.isGoalState(current_node.position):
            return reconstruct_path(current_node)

        if current_node.position not in visited:
            visited.add(current_node.position)

            for successor, action, step_cost in problem.getSuccessors(
                    current_node.position
            ):
                if successor not in visited:
                    successor_node = SearchNode(
                        position=successor,
                        parent=current_node,
                        action=action,
                        path_cost=current_node.path_cost + step_cost
                    )
                    fringe.push(successor_node)

    return []


def reconstruct_path(goal_node):
    path = []
    while goal_node.action is not None:  # Assuming the start node has None
        # as its action
        path.append(goal_node.action)
        goal_node = goal_node.parent
    path.reverse()
    return path


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(
    problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    return generic_search(problem, stack)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    return generic_search(problem, queue)


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    def path_cost(search_node: SearchNode):
        return search_node.path_cost

    path_cost_priority_queue = util.PriorityQueueWithFunction(path_cost)

    return generic_search(problem, path_cost_priority_queue)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the
    nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic
    first."""
    "*** YOUR CODE HERE ***"

    def a_star_priority_function(node: SearchNode):
        """A* optimizes for f(n) = g(n) + h(n)"""
        g_n = node.path_cost
        h_n = heuristic(node.position, problem)
        return g_n + h_n

    a_star_priority_queue = util.PriorityQueueWithFunction(
        a_star_priority_function
    )

    return generic_search(problem, a_star_priority_queue)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
