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

# Ana Ortiz 01524018
# Alexa Zambrano 


from util import manhattanDistance
from game import Directions
from game import Grid
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        
        # food nearby: makes move more appealing 
        # ghost nearby: makes move less appealing 
        # scared ghost nearby: makes move more appealing 

        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPacPos = successorGameState.getPacmanPosition()
        newGhostStates = successorGameState.getGhostStates()
        newGhostPos = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newNumFood = successorGameState.getNumFood()
        newFood = successorGameState.getFood()
        coordPairFood = newFood.asList()
        

        score: int
        score = successorGameState.getScore()

        # use manhattan distance formula to calcualte the distance between pacman, food, and ghosts
        smallestFoodDistance = float('inf')
        smallestGhostDistance = float('inf')

        # check if pacman is close to food 
        #check if the list is empty 
        if coordPairFood:
            for coordinate in coordPairFood:
                pacAndFoodDistance : int = util.manhattanDistance(newPacPos, coordinate)
                if smallestFoodDistance > pacAndFoodDistance:
                    smallestFoodDistance = pacAndFoodDistance

        # check if pacman is close to ghosts 
        # check whether ghost is active or scared 
        for ghostState in newGhostStates:
                
            pacAndGhostDistance : int = util.manhattanDistance(newPacPos, newGhostStates)
            

            



        # something good: being closer to food -> add to evaluation 

        # something not good: being close to an active ghost -> subtract from the evaluation 
        



        print("grid of new food:", newFood)
        print("number of new food:", newNumFood)
        print("coordinate pair of new food:", coordPairFood)
        print("position of pacman after moving:", newPacPos)
        print("number of moves that each ghost will remain scared after pacman ate a power pallet:", newScaredTimes)
        print("new ghost states: ", newGhostStates)

        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
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
        
    # max value implementation - handles pacman's turn
    # compares the values of possible successor states and returns the highest
    def maxValue(gameState: GameState, agentIndex: int, currentDepth: int):
    
        return v
    
    
    # min value implementation - ghosts 
    # compares the values of possible successor states and returns the lowest
    def minValue(gameState: GameState, agentIndex: int, currentDepth: int):


        return v
    


    # value implementation 
    # first checks whether the search should stop: depth limit is reached OR game has ended - pacman wins or loses before that limit 
    # when either happens, stop exploring that branch and use self.evaluationFunction to score its current state 
    # if pacmans's turn -> use MAX value
    # else it's ghost's turn -> use MIN value 
    # current depth = completed rounds along this branch 
    def value(self, gameState: GameState, agentIndex: int, currentDepth: int):

        # check if the game has ended 
        # check if the current depth reaches or exceeds the limit 
        # return evaluation score for the current state 
        if gameState.isWin() or gameState.isLose() or currentDepth >=  self.depth:
            return self.evaluationFunction
        
        # if stopping check is false, decide whose turn it is

        # pacman's turn 
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, currentDepth)
        # ghost's turn 
        else:
            return self.minValue(gameState, agentIndex, currentDepth)

    

    def getAction(self, gameState: GameState):
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
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
