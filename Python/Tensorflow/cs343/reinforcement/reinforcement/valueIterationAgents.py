# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # repreats iteration times updating the values to get the right policy and values
        for _ in xrange(0, iterations):
            # keeps a copy so that the values are updated independently during single iteration
            counterCopy = self.values.copy()
            for state in mdp.getStates():
                maxVal = -999999
                # loops through to find the maximum value of the possible actions
                for action in self.mdp.getPossibleActions(state):
                    qVal = self.computeQValueFromValues(state, action)
                    if (qVal > maxVal):
                        maxVal = qVal
                if (maxVal == -999999):
                    maxVal = self.getValue(state)
                counterCopy[state] = maxVal
            self.values = counterCopy

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
          
          V(s) = max_{a in actions} Q(s,a) = self.values
          
          
          Should return Q(state,action)
          Q*(state, action) = sum[s'](T(s,a,s') * (R(s,a,s') + discount * V(s')))
        """
        "*** YOUR CODE HERE ***"
        qVal = 0
        # finds QVal accorind to Q*(state, action) = sum[s'](T(s,a,s') * (R(s,a,s') + discount * V(s')))
        for newState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            qVal += prob * (self.mdp.getReward(state, action, newState) + self.discount * self.getValue(newState))
        return qVal

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.

          policy(s) = arg_max_{a in actions} Q(s,a)
        """
        "*** YOUR CODE HERE ***"
        maxAction = []
        maxVal = -999999
        # returns best action according to arg_max_{a in actions} Q(s,a)
        for action in self.mdp.getPossibleActions(state):
            val = self.computeQValueFromValues(state, action)
            if (val > maxVal):
                maxVal = val
                maxAction = action
        return maxAction      

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
