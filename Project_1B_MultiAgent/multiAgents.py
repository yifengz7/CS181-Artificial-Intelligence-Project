# multiAgents.py
# --------------
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
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        return successorGameState.getScore()

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
      Your minimax agent (question 1)
    """



    def getAction(self, currentState):


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

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        # Get all the legal actions and their values
        legalActions = currentState.getLegalActions(self.index)
        valuesForLegalActions = [self.value(currentState.generateSuccessor(0, action), 1, 0) for action in legalActions]

        # Return the action with the largest value, since Pacman is a max agent
        maxValue = max(valuesForLegalActions)
        bestIndex = valuesForLegalActions.index(maxValue)
        return legalActions[bestIndex]



    def value(self, currentState, agentIndex, currentDepth):
        # If it is terminal state, return utility of the state
        if currentDepth == self.depth or currentState.isWin() or currentState.isLose():
            return self.evaluationFunction(currentState)
        # If it is pacman (max agent), return max-value
        if agentIndex == 0:
            return self.maxValue(currentState, agentIndex, currentDepth)
        # Else it is ghost (min agent), return min-value
        else:
            return self.minValue(currentState, agentIndex, currentDepth)


    def maxValue(self, currentState, agentIndex, currentDepth):
        assert agentIndex == 0
        v = float("-inf")
        legalActions = currentState.getLegalActions(agentIndex)
        legalSuccesors = [currentState.generateSuccessor(agentIndex, action) for action in legalActions]
        nextAgent = agentIndex + 1
        nextDepth = currentDepth
        # for each successor of state, find the maximum value among them
        for successor in legalSuccesors:
            v = max(v, self.value(successor, nextAgent, nextDepth))
        return v


    def minValue(self, currentState, agentIndex, currentDepth):
        lastGhostAgent = currentState.getNumAgents() - 1
        v = float("+inf")
        legalActions = currentState.getLegalActions(agentIndex)
        legalSuccesors = [currentState.generateSuccessor(agentIndex, action) for action in legalActions]
        nextAgent = agentIndex + 1 if agentIndex != lastGhostAgent else 0
        nextDepth = currentDepth + 1 if agentIndex == lastGhostAgent else currentDepth
        # for each successor of state, find the minimum value among them
        for successor in legalSuccesors:
            v = min(v, self.value(successor, nextAgent, nextDepth))
        return v










class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 2)
    """

    def getAction(self, currentState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # Get all the legal actions and their values
        legalActions = currentState.getLegalActions(self.index)
        alpha = float("-inf")
        beta = float("+inf")
        valuesForLegalActions = []
        nextAgent = self.index + 1

        for action in legalActions:
            v = self.value(currentState.generateSuccessor(self.index, action), nextAgent, 0, alpha, beta)
            valuesForLegalActions.append(v)
            if v > beta:
                break
            alpha = max(alpha, v)

        # Return the action with the largest value, since Pacman is a max agent
        maxValue = max(valuesForLegalActions)
        bestIndex = valuesForLegalActions.index(maxValue)
        return legalActions[bestIndex]




    def value(self, currentState, agentIndex, currentDepth, alpha, beta):
        # If it is terminal state, return utility of the state
        if currentDepth == self.depth or currentState.isWin() or currentState.isLose():
            return self.evaluationFunction(currentState)
        # If it is pacman (max agent), return max-value
        if agentIndex == 0:
            return self.maxValue(currentState, agentIndex, currentDepth, alpha, beta)
        # Else it is ghost (min agent), return min-value
        else:
            return self.minValue(currentState, agentIndex, currentDepth, alpha, beta)


    def maxValue(self, currentState, agentIndex, currentDepth, alpha, beta):
        assert agentIndex == 0
        v = float("-inf")
        legalActions = currentState.getLegalActions(agentIndex)
        nextAgent = agentIndex + 1
        nextDepth = currentDepth
        # for each successor of state, find the maximum value among them
        for action in legalActions:
            v = max(v, self.value(currentState.generateSuccessor(agentIndex, action), nextAgent, nextDepth, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v


    def minValue(self, currentState, agentIndex, currentDepth, alpha, beta):
        lastGhostAgent = currentState.getNumAgents() - 1
        v = float("+inf")
        legalActions = currentState.getLegalActions(agentIndex)
        nextAgent = agentIndex + 1 if agentIndex != lastGhostAgent else 0
        nextDepth = currentDepth + 1 if agentIndex == lastGhostAgent else currentDepth
        # for each successor of state, find the minimum value among them
        for action in legalActions:
            v = min(v, self.value(currentState.generateSuccessor(agentIndex, action), nextAgent, nextDepth, alpha, beta))
            if v < alpha:
                return v
            beta = min(beta, v)
        return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """

    def getAction(self, currentState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        legalActions = currentState.getLegalActions(self.index)
        valuesForLegalActions = []
        nextAgent = self.index + 1
        for action in legalActions:
            v = self.value(currentState.generateSuccessor(self.index, action), nextAgent, 0)
            valuesForLegalActions.append(v)

        # Return the action with the largest value, since Pacman is a max agent
        maxValue = max(valuesForLegalActions)
        bestIndex = valuesForLegalActions.index(maxValue)
        return legalActions[bestIndex]

    def value(self, currentState, agentIndex, currentDepth):
        # If it is terminal state, return utility of the state
        if currentDepth == self.depth or currentState.isWin() or currentState.isLose():
            return self.evaluationFunction(currentState)
        # If it is pacman (max agent), return max-value
        if agentIndex == 0:
            return self.maxValue(currentState, agentIndex, currentDepth)
        # Else it is ghost (min agent), return min-value
        else:
            return self.expectedValue(currentState, agentIndex, currentDepth)

    def maxValue(self, currentState, agentIndex, currentDepth):
        assert agentIndex == 0
        v = float("-inf")
        legalActions = currentState.getLegalActions(agentIndex)
        nextAgent = agentIndex + 1
        nextDepth = currentDepth
        # for each successor of state, find the maximum value among them
        for action in legalActions:
            v = max(v, self.value(currentState.generateSuccessor(agentIndex, action), nextAgent, nextDepth))
        return v

    def expectedValue(self, currentState, agentIndex, currentDepth):
        lastGhostAgent = currentState.getNumAgents() - 1
        v = 0.0
        legalActions = currentState.getLegalActions(agentIndex)
        nextAgent = agentIndex + 1 if agentIndex != lastGhostAgent else 0
        nextDepth = currentDepth + 1 if agentIndex == lastGhostAgent else currentDepth
        # for each successor of state, find the minimum value among them
        for action in legalActions:
            v += self.value(currentState.generateSuccessor(agentIndex, action), nextAgent, nextDepth)
        v /= len(legalActions)
        return v



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 4).

      DESCRIPTION:

        For all the parts of the score:
            if negative, then the smaller the part is, the better
            if positive, then the larger the part is, the better

        Smaller-better parts:
            Number of left foods
            Distance to closest food
            Distance to closest real ghost

        Larger-better parts:
            Distance to closest fake ghost






    """
    "*** YOUR CODE HERE ***"

    score = currentGameState.getScore()

    position = currentGameState.getPacmanPosition()

    foods = currentGameState.getFood()

    # The less food left, the better.

    # So motivate Pacman to find food
    closestFood = min([manhattanDistance(position, food) for food in foods]) if foods else 0
    score -= 2*closestFood

    # And eat them
    numOfFoods = currentGameState.getNumFood()
    score -= 5*numOfFoods


    ghostStates = currentGameState.getGhostStates()

    ghostPositions = currentGameState.getGhostPositions()

    # Bool
    scaredGhost = False

    for ghost in ghostStates:
        # Ghost is active, motivate Pacman to run away from it
        if ghost.scaredTimer == 0:
            score -= 12*manhattanDistance(position, ghost.getPosition())
        # Ghost is scared, go get 'em!
        else:
            score += manhattanDistance(position, ghost.getPosition())
            scaredGhost = True

    # If there is no scare ghost, motivate Pacman to go for capsules
    if not scaredGhost:
        capsules = currentGameState.getCapsules()
        closestCapsule = min([manhattanDistance(position, capsule) for capsule in capsules]) if capsules else 0
        numOfCapsule = len(capsules)
        score -= .65*(numOfCapsule + closestCapsule)


    return score







# Abbreviation
better = betterEvaluationFunction
