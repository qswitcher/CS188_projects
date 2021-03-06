# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()

        ghostContrib = -1*min([1.0/(util.manhattanDistance(newPos, ghost.getPosition()) + 1) for ghost in newGhostStates])
        foodArray = [1.0/(util.manhattanDistance(newPos, food) + 1) for food in newFood.asList()]
        if not foodArray:
            foodArray = [1]
        foodContrib = max(foodArray)
        scoreContrib = (successorGameState.getScore() - currentGameState.getScore())


        value = scoreContrib + ghostContrib + foodContrib
        return value

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        max_action = None
        max_v = None
        for action in gameState.getLegalActions(self.index):
            result = self.maxValue(gameState, action, self.depth, self.index + 1)[self.index]
            if result > max_v:
                max_v = result
                max_action = action
        return max_action

    def maxValue(self, gameState, action, depth, agent_index):
        """
        Maximizes value of the 'agent_index'th agent
        """
        if not depth:
            return self.getV(gameState)

        # generate the next gamestate resulting from this action
        newGameState = gameState.generateSuccessor(agent_index - 1, action)
        if newGameState.isWin() or newGameState.isLose():
            return self.getV(newGameState)

        v = None
        for action in newGameState.getLegalActions(agent_index):
            result = self.maxValue(newGameState, action,
                                  depth - 1 if agent_index == self.index else depth,
                                  (agent_index + 1) % gameState.getNumAgents())
            # print "v: " + str(v)
            # print "result: " + str(result)
            # print "agent: " + str(agent_index)
            v = result if v is None else max(v, result, key=lambda(x): x[agent_index])
        return v

    def getV(self, gameState):
        value = gameState.getNumAgents()*[-1*self.evaluationFunction(gameState),]
        value[self.index] *= -1
        return value


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        max_action = None
        max_v = None
        alpha = -float('inf')
        beta = float('inf')
        for action in gameState.getLegalActions(self.index):
            result = self.optimalValue(gameState, action, self.depth, self.index + 1, alpha, beta)
            if result > max_v:
                max_v = result
                max_action = action
            alpha = max(alpha, result)
        return max_action

    def optimalValue(self, gameState, action, depth, agent_index, alpha, beta):
        """
        Maximizes value of the 'agent_index'th agent
        """
        if not depth:
            return self.getV(gameState)

        # generate the next gamestate resulting from this action
        newGameState = gameState.generateSuccessor(agent_index - 1, action)
        if newGameState.isWin() or newGameState.isLose():
            return self.getV(newGameState)

        v = -float('inf') if self.index == agent_index else float('inf')
        for action in newGameState.getLegalActions(agent_index):
            result = self.optimalValue(newGameState, action,
                                  depth - 1 if agent_index == self.index else depth,
                                  (agent_index + 1) % gameState.getNumAgents(),
                                  alpha, beta)

            if agent_index == self.index:
                v = max(v, result)
                if v > beta:
                    return v
                alpha = max(alpha, v)
            else:
                v = min(v, result)
                if v < alpha:
                    return v
                beta = min(beta, v)
        return v

    def getV(self, gameState):
        return self.evaluationFunction(gameState)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        max_action = None
        max_v = None
        for action in gameState.getLegalActions(self.index):
            result = self.maxValue(gameState, action, self.depth, self.index + 1)
            if result > max_v:
                max_v = result
                max_action = action
        return max_action

    def maxValue(self, gameState, action, depth, agent_index):
        """
        Maximizes value of the 'agent_index'th agent
        """
        if not depth:
            return self.getV(gameState)

        # generate the next gamestate resulting from this action
        newGameState = gameState.generateSuccessor(agent_index - 1, action)
        if newGameState.isWin() or newGameState.isLose():
            return self.getV(newGameState)

        v = None
        actions = newGameState.getLegalActions(agent_index)
        for action in actions:
            result = self.maxValue(newGameState, action,
                                  depth - 1 if agent_index == self.index else depth,
                                  (agent_index + 1) % gameState.getNumAgents())
            if self.index == agent_index:
                v = result if v is None else max(v, result)
            else:
                if v is None:
                    v = (1.0/len(actions))*result
                else:
                    v += (1.0/len(actions))*result
        return v

    def getV(self, gameState):
        return self.evaluationFunction(gameState)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    pos = currentGameState.getPacmanPosition()
    foodGrid = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()

    closet_ghost_pos = None
    ghostContrib = 0
    for ghost in ghostStates:
        ghost_pos = util.manhattanDistance(pos, ghost.getPosition())
        closet_ghost_pos = ghost_pos if not closet_ghost_pos or ghost_pos < closet_ghost_pos else closet_ghost_pos

        ghostContrib = -0.5*1.0/(closet_ghost_pos + 1)
        if ghost.scaredTimer:
            ghostContrib *= -2

    # compute food contrib
    closest_food = None
    closest_food_distance = None
    for food in foodGrid.asList():
        food_distance = util.manhattanDistance(pos, food)
        if not closest_food or closest_food_distance > food_distance:
            closest_food_distance = food_distance
            closest_food = food

    if not closest_food_distance:
        closest_food_distance = 1000000
    foodContrib = 1.0/closest_food_distance - 2.1*len(foodGrid.asList())

    # is a wall in our way?
    wall_contrib = 0
    if closest_food:
        if closest_food[0] < pos[0]:
            if currentGameState.hasWall(pos[0] - 1, pos[1]):
                wall_contrib -= 1
        elif closest_food[0] > pos[0]:
            if currentGameState.hasWall(pos[0] + 1, pos[1]):
                wall_contrib -= 1
        elif closest_food[1] < pos[1]:
            if currentGameState.hasWall(pos[0], pos[1] - 1):
                wall_contrib -= 1
        elif closest_food[1] > pos[1]:
            if currentGameState.hasWall(pos[0], pos[1] + 1):
                wall_contrib -= 1

    # find closest power pellet
    powerPelletContrib = [1.0/util.manhattanDistance(pos, pellet) for pellet in currentGameState.getCapsules()]
    if not powerPelletContrib:
        powerPelletContrib = 0
    else:
        powerPelletContrib = 0.9*min(powerPelletContrib)

    value = 0.5*wall_contrib + foodContrib + ghostContrib + 10*currentGameState.getScore() + powerPelletContrib

    return value

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

