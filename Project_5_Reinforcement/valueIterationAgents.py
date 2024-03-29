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
import collections

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
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        # Q1
        numIter = self.iterations
        for i in range(numIter):
            newVals = util.Counter()
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state):
                    continue
                actions = self.mdp.getPossibleActions(state)
                bestVal = max([self.getQValue(state, action) for action in actions])
                newVals[state] = bestVal
            self.values = newVals



    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # Q1
        statesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        q = 0
        for nextState, p in statesAndProbs:
            reward = self.mdp.getReward(state, action, nextState)
            q += p * (reward + self.discount * self.values[nextState])
        return q


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # Q1
        if self.mdp.isTerminal(state):
            return None
        actions = self.mdp.getPossibleActions(state)
        policy = util.Counter()
        for action in actions:
            policy[action] = self.getQValue(state, action)
        return policy.argMax()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        # Q4
        states = self.mdp.getStates()
        numStates = len(states)
        numIter = self.iterations
        for i in range(numIter):
            state = states[i % numStates]
            if self.mdp.isTerminal(state):
                continue
            actions = self.mdp.getPossibleActions(state)
            bestVal = max([self.getQValue(state, action) for action in actions])
            self.values[state] = bestVal

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)



    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        # Q5
        preds = {}
        states = [state for state in self.mdp.getStates() if not self.mdp.isTerminal(state)]
        for state in states:
            actions = self.mdp.getPossibleActions(state)
            for action in actions:
                for nextState, p in self.mdp.getTransitionStatesAndProbs(state, action):
                    if nextState in preds:
                        preds[nextState].add(state)
                    else:
                        preds[nextState] = {state}

        queue = util.PriorityQueue()
        states = [state for state in self.mdp.getStates() if not self.mdp.isTerminal(state)]
        numIter = self.iterations

        for state in states:
            maxQ = max([self.getQValue(state, action) for action in self.mdp.getPossibleActions(state)])
            diff = abs(self.values[state] - maxQ)
            queue.push(state, -diff)


        for i in range(numIter):

            if queue.isEmpty():
                break

            state = queue.pop()

            if self.mdp.isTerminal(state):
                continue

            maxQ = max([self.getQValue(state, action) for action in self.mdp.getPossibleActions(state)])
            self.values[state] = maxQ

            for pred in preds[state]:
                if not self.mdp.isTerminal(pred):
                    maxQ = max([self.getQValue(pred, action) for action in self.mdp.getPossibleActions(pred)])
                    diff = abs(self.values[pred] - maxQ)
                    if diff > self.theta:
                        queue.update(pred, -diff)
