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
from operator import pos
from Tkconstants import CURRENT

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
        "*** YOUR CODE HERE ***"  
        capsules = currentGameState.getCapsules()
        foodList = currentGameState.getFood().asList()
        curPos = currentGameState.getPacmanPosition()
        intMax = 999999
        scoreNumerator = 100
        runAway = 3
        # test arguments = --frameTime 0 -p ReflexAgent -k 2
        # finds the closest food and uses this to add to the score
        minDistanceToFood = intMax
        for food in foodList:
            dis = euclideanDistance(food, newPos)
            if dis < minDistanceToFood and newPos != curPos:
                minDistanceToFood = dis
        if minDistanceToFood > 0:
            heuristicClosest = scoreNumerator / minDistanceToFood
        else:
            heuristicClosest = scoreNumerator
         
        # runs away from a ghost in the farthest position it it is within the run away constant   
        for ghostState in newGhostStates:
            dis = manHattanDistance(newPos, ghostState.getPosition())
            capEaten = ghostState.scaredTimer > 0
            if (not capEaten and dis < runAway):
                return dis
            
        # checks if next position is a capsul and returns a higher score than if it was a food
        if newPos in capsules:
            return successorGameState.getScore() + scoreNumerator + 1
        
        return successorGameState.getScore() + heuristicClosest 

# returns the Manhattan distance between two points
def manHattanDistance (xy1, xy2):
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

# returns the euclidean distance between two points
def euclideanDistance (xy1, xy2):
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

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
          Returns the minimax action from the current gameState using 
          
          -self.depth
          -self.evaluationFunction

          Here are some method calls that might be useful when implementing minimax.

          -gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          -gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          -gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # initially calls the minVal function to start this algorithm
        maxVal = -999999
        for action in gameState.getLegalActions(0):
            newState = gameState.generateSuccessor(0, action)
            temp = 0
            temp = self.minVal(newState, 1, 0)
            if maxVal < temp:
                maxVal = temp
                maxAction = action
        return maxAction
    
    # this is the function for pacman to maximize the score
    def  maxVal(self, gameState, depth):
        if not gameState.getLegalActions(0) or depth >= self.depth:
            return self.evaluationFunction(gameState)
        v = -999999
        for action in gameState.getLegalActions(0):
            newState = gameState.generateSuccessor(0, action)
            temp = 0
            temp = self.minVal(newState, 1, depth)
            v = max(v, temp)
        return v
    
    # this is the function for the ghosts to minimize the score
    def  minVal(self, gameState, ghostIndex, depth):
        if not gameState.getLegalActions(0) or depth >= self.depth:
            return self.evaluationFunction(gameState)
        v = 999999
        for action in gameState.getLegalActions(ghostIndex):
            newState = gameState.generateSuccessor(ghostIndex, action)
            if (ghostIndex >= gameState.getNumAgents() - 1):
                v = min(v, self.maxVal(newState, depth + 1))
            else:
                v = min(v, self.minVal(newState, ghostIndex + 1, depth))
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -999999
        beta = 999999
        v = self.maxValAB(gameState, alpha, beta, 0)
        actionMax = -999999
        # initially calls the minValAB function and stores alpha
        for action in gameState.getLegalActions(0):
            newState = gameState.generateSuccessor(0, action)
            temp = self.minValAB(newState, alpha, beta, 0, 1)
            if temp == v:
                maxAction = action
            alpha = max (alpha, temp)
        return maxAction
        
    # this should be the pacman agent
    def maxValAB(self, gameState, alpha, beta, depth):
        if not gameState.getLegalActions(0) or depth >= self.depth:
            return self.evaluationFunction(gameState)
        v = -999999
        for action in gameState.getLegalActions(0):
            newState = gameState.generateSuccessor(0, action)
            v = max(v, self.minValAB(newState, alpha, beta, depth, 1))
            if v > beta:
                return v
            alpha = max (alpha, v)
        return v
    
    # this should be the ghost agent
    def minValAB(self, gameState, alpha, beta, depth, ghostIndex):
        if not gameState.getLegalActions(ghostIndex) or depth >= self.depth:
            return self.evaluationFunction(gameState)
        v = 999999
        for action in gameState.getLegalActions(ghostIndex):
            newState = gameState.generateSuccessor(ghostIndex, action)
            if (ghostIndex >= gameState.getNumAgents() - 1):
                v = min(v, self.maxValAB(newState, alpha, beta, depth + 1))
            else:
                v = min(v, self.minValAB(newState, alpha, beta, depth, ghostIndex + 1))
            if v < alpha: 
                return v
            beta = min(beta, v)
        return v

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
        "*** YOUR CODE HERE ***"
        v = -999999
        for action in gameState.getLegalActions(0):
            newState = gameState.generateSuccessor(0, action)
            temp = self.expVal(newState, 0, 1)
            if temp > v:
                maxAction = action
                v = temp
        return maxAction
        
        
    # this is pacmans Max function
    def maxValE (self, gameState, depth):
        if not gameState.getLegalActions(0) or depth >= self.depth:
            return self.evaluationFunction(gameState)
        v = -999999
        listOfActions = gameState.getLegalActions(0)
        for action in listOfActions:
            newState = gameState.generateSuccessor(0, action)
            v = max(v, self.expVal(newState, depth, 1))
        return v
        
    # these are the ghosts expectimax function, taking the average of its scores     
    def expVal (self, gameState, depth, ghostIndex):
        if not gameState.getLegalActions(ghostIndex) or depth >= self.depth:
            return self.evaluationFunction(gameState)
        v = 0
        listOfActions = gameState.getLegalActions(ghostIndex)
        for action in listOfActions:
            newState = gameState.generateSuccessor(ghostIndex, action)
            p = 1.0 / len(listOfActions)
            if (ghostIndex >= gameState.getNumAgents() - 1):
                v += p * self.maxValE(newState, depth + 1)
            else:
                v += p * self.expVal(newState, depth, ghostIndex + 1)
        return v

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: I used four variables in determining the 
        new evaluation function. These four were the two furthests food dots and 
        pacmans distance to the closest of these two, the distance to the nearest
        ghost, the distance to the nearest capsule, and the score. I combined these
        for a linear sum, taking an appropriate percentage of each to maximize the
        score of pacman. 
    """
    "*** YOUR CODE HERE ***"
    score = 0
    foodList = currentGameState.getFood().asList()
    currentPos = currentGameState.getPacmanPosition()
    maxDistance = 1
    minCap = 999999
    minGhost = 999999
    # gets closest ghost
    for pos in currentGameState.getGhostPositions():
        minGhost = min(minGhost, manHattanDistance(pos, currentPos))
    
    # gets closest capsule
    for pos in currentGameState.getCapsules():
        minCap = min(minCap, manHattanDistance(pos, currentPos))
    
    # gets two farthest food dots and pacmans distance to the closest of these two
    for pos in foodList:
        for pos2 in foodList:
            dis = manhattanDistance(pos, pos2)
            maxDistance = max (maxDistance, max(manHattanDistance(currentPos, pos) + dis, manHattanDistance(currentPos, pos2) + dis))
    
    score += currentGameState.getScore() * 0.3
    score += (100 / maxDistance) * 0.3
    score += (100 / minCap) * 0.2  
    score += (minGhost) * 0.2
    
    return score

# Abbreviation
better = betterEvaluationFunction

