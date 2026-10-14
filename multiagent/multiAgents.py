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
        newGhostPos = successorGameState.getGhostPosition(1)
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
                
            pacAndGhostDistance : int = util.manhattanDistance(newPacPos, newGhostPos)
            

            



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
            return self.evaluationFunction(gameState)
        
        # if stopping check is false, decide whose turn it is

        # pacman's turn 
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, currentDepth)
        # ghost's turn 
        else:
            return self.minValue(gameState, agentIndex, currentDepth)

        
    # max value implementation - handles pacman's turn
    # compares the values of possible successor states and returns the highest
    def maxValue(self, gameState: GameState, agentIndex: int, currentDepth: int):

        highestValue = float('-inf')

        # explore each legal pacman action and generate its successor state 
        for action in gameState.getLegalActions(0):
            successorGameState = gameState.generateSuccessor(0, action)

            # evaluate successor 
            successorValue = self.value(successorGameState, 1, currentDepth)
            if successorValue > highestValue:
                highestValue = successorValue


        return highestValue
    
    
    # min value implementation - ghosts 
    # compares the values of possible successor states and returns the lowest
    def minValue(self, gameState: GameState, agentIndex: int, currentDepth: int):

        lowestValue = float('inf')

        # explore each legal pacman action and generate its successor state 
        # evaluate successor -> loop over current ghost's legal actions 
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)

            # need to check whether current ghost is the last agent -> if there are more ghosts
            # depth is incremented
            if agentIndex == gameState.getNumAgents() - 1:   
                successorValue = self.value(successorGameState, 0, currentDepth + 1)
                if successorValue < lowestValue:
                    lowestValue = successorValue

            # this isn't the last ghost
            # depth does not change
            else:
                successorValue = self.value(successorGameState, agentIndex + 1, currentDepth)
                if successorValue < lowestValue:
                    lowestValue = successorValue
            
        return lowestValue
    

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
        ""

        highestValue = float('-inf')
        bestAction = None

        # explore each legal pacman action and generate its successor state 
        for action in gameState.getLegalActions(0):
            successorGameState = gameState.generateSuccessor(0, action)

            # evaluate successor 
            successorValue = self.value(successorGameState, 1, 0)
            if successorValue > highestValue:
                highestValue = successorValue
                bestAction = action


        return bestAction


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
       

        """

        self.depth = search depth or like rounds 
        self.evalutaionFunction = to score a game state when 
        gameState = where the game is at
        0 = pacman

        this method returns the final action based on what it gets 
        
        
        """

        legal_moves = gameState.getLegalActions(0); 
        best_move = None;
        best_score  = float('-inf');

        for action in legal_moves:

            futureState = gameState.generateSuccessor(0, action)

            score = self.value(futureState, agent=1, depth=0)

            if score > best_score:

                best_score = score
                best_move = action

        return best_move





    def value (self, gameState, agent, depth):
        '''
        pseudocode from slides:
        
                def value (state):
                if the state is a terminal state: 
                    return the state's utility 
                    if the next agent is MAX: 
                    return max-value(state) 
                    if the next agent is EXP: 
                    return exp-value(state)
        '''
        #if terminated
        if gameState.isLose() or gameState.isWin() or depth == self.depth:
            return self.evaluationFunction(gameState) #share the current score 

        if agent == 0:
            #pacman's turn
            return self.max_value(gameState, agent, depth)
        else:
            #ghost's turn
            return self.exp_value(gameState, agent, depth)

        

    #pacmans choice
    def max_value(self, gameState: GameState, agent, depth = 0):

         """
         pseudo from slides:

         def max-value(state):
            initialize v = -o0
            for each successor of state:
            v = maxv, value(successor))
            return v
         """
        #pacman turn

        
         v = float('-inf')
        
         legal_actions = gameState.getLegalActions(agent);

         
        #for every succesor state
         for action in legal_actions:
             successor = gameState.generateSuccessor(agent, action)

             #pick value
             v = max(v, self.value(successor, agent = 1, depth=depth))

         return v



    # Ghost 
    def exp_value(self, gameState: GameState, agent, depth): #ghost
        '''
        def exp-value(state):
            initialize v = 0
            for each successor of state:
            p = probability(successor)
            v += p * value(successor)
        return v
        '''
        
        v = 0

        legal_actions = gameState.getLegalActions(agent);

        if not legal_actions:
            return self.evaluationFunction(gameState)

        #probability
        p = (1.0/len(legal_actions))

        #find next agent after turn  because there could be multiple ghosts :()
        num_agents=gameState.getNumAgents()
        next_agent = agent + 1
        next_depth = depth;

        #if not more agents then go back to pacman
        if next_agent == num_agents:
            '''
                since no more exp agents we have to go to another rround and start with pacaman

            '''
            next_agent = 0
            next_depth = depth + 1

        
        #for every action check the state of the agent in that action 
        for action in legal_actions:

            successor = gameState.generateSuccessor(agent, action)

            # expected value 
            v += p * self.value(successor, next_agent, next_depth) #redirect this value to decide if we use exp or max
        
        return v 
        #util.raiseNotDefined()

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
