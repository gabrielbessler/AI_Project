#TODO:need state class so that this can work
#TODO:state class needs to know if terminal, and what turn it is
#TODO:when we expand from leaf, we add one edge to another node.
#TODO:state class also needs function that gets available actions
import math
import tictactoe.py

class MCTS:
    "Monte Carlo tree searcher."

    #c is some tunable parameter that helps select what node to progress to
    #TODO: takes in some model. can call model.predict() and model.update()
    def __init__(self, root_state, game, model, c=1):
        self.W = dict()  # total reward of taking action from state
        self.Q = dict() # average reward of taking action from state
        self.N = dict() # total visit count of taking action from state
        self.actions = dict()  # possible actions for each state, each state corresponding to a list
        self.num_actions = dict() #number of possible actions for each state
        self.child = dict() #expanded children of each possible action for each node
        self.c = c
        #setting up the initial root state
        self.root = root_state
        self.initalize(root_state)
        # we get this policy from the nnet, of probabilites of actions given a state
        self.policy = dict()
        self.path = []
        self.game = game
        self.model = model

    #must be called every time we want to evaluate with MCTS after the intialization
    def set_root(self,state):
        self.root = state

    def initalize(self,state):
        self.actions[root_state] = []
        self.policy[root_state] = dict()

    #after intialization, this will be the MAIN function that is called
    def perform_iterations(self,numIterations):
        for i in range(numIterations):
            self.perform_iteration()

    #an iteration of the MCTS
    def perform_iteration(self):
        #first, we simulate playing from the root node until we get to a leaf of the game tree.
        #A leaf state is a state we have not explored further from.
        leaf_state = self.select_leaf()
        #then, we check to see if the leaf is a terminal state
        terminal_value = self.get_terminal_value(leaf_state)
        if ((terminal_value != 0) or ((terminal_value == 0) and (len(game.getAllActions()) == 0))):
            #if it is a terminal state, then we check to see
            #how the value of the game at this terminal compares to the
            #neural net's predicted value of the root node
            #we train the neural net based on this comparison
            leaf_value = terminal_value
            # we then backpropagate these results back up the tree to the root
            self.backpropagate(leaf_value)
            # TODO: do we need this? or just calling it from the policy dictionary if backprop computes
            # this for each node it traversed? Is backprop even doing that?
            pi = self.get_action_prob_dist()
            #TODO: get probability vector distribution from number of times perfomed actions
            #TODO update nn so that predicted value  and prob dist is not so different actual score
            self.model.update(pi, leaf_value)
            # and probabiliy distribution for the actions taken
            # don't actually know how to integrate that here

        else:
            #if it is not a terminal state, then we expand the possible children of the node,
            #and take the action dictated by the neural net
            leaf_value = self.expand_leaf(leaf_state)
            # we then backpropagate these results back up the tree to the root
            self.backpropagate(leaf_value)

    def get_action_prob_dist(self):
        prob_dist = []
        num_total_actions = 0
        for action in actions[self.root]:
            num_total_actions += self.N[self.root][action]
        for action in actions[self.root]:
            prob_dist.append(self.N[self.root][action]/num_total_actions)
        return prob_dist

    def get_terminal_value(self, state):
        self.game.board = state.board
        self.game.currPlayer = state.currPlayer
        return self.game.checkGameOver()

    def select_leaf(self):
        current_state = self.root
        while not self.is_leaf(current_state):
            best_action = self.choose_action[current_state]
            #see if we taken action before, if not, add the child to the dictionary:
            if best_action not in self.child[current_state]:
                #gets state from new board based on action
                simulated_state = self.simulate_action(best_action)
                #initializes this new state
                self.initalize(simulated_state)
                self.child[current_state][best_action] = simulated_state
            path_tuple = (current_state, best_action)
            self.path.append(path_tuple)
            current_state = self.child[current_state][best_action]

        return current_state

    def simulate_action(self, state):
        child = Node(copy.deepcopy(state.board))
        child.currPlayer = self.game.turnChooser(state.currPlayer)
        pieceToPlay = 1 if state.currPlayer == 0 else 2
        child.board[action[0]][action[1]][action[2]] = pieceToPlay
        return child

    def is_leaf(self,state):
        #if the actions dictionary of the state is empty, then it's a leaf
        if len(self.actions[state]) == 0:
            return True
        else:
            return False

    def choose_action(self, state):
        #chooses action by UCT value
        total_n = 0
        for action in self.actions[state]:
            total_n += self.N[state][action]
        action_values = dict()
        for action in self.actions[state]:
            # for the policy, do we ask the neural net each time what it is?
            #or do we ask once and save?
            #or use the policy computed by backprop at the end
            action_values[action] = self.Q[state][action] + (self.c * self.policy[state][action] * math.sqrt(math.log(total_n) / (1 + self.N[state][action])))
        return max(action_values, key=action_values.get())

    def expand_leaf(self, state):
        self.actions[root_state] = root_state.getAllActions()
        #initalize the dictionary of each action's child from the root state
        # the dictionary gets filled out as we take each action.
        self.child[state] = dict()
        if len(self.actions[state] > 0:
            self.N[state] = dict()
            self.W[state] = dict()
            self.Q[state] = dict()
        for action in self.actions[state]:
            self.N[state][action] = 0
            self.W[state][action] = 0
            self.Q[state][action] = 0
        #TODO: figure out which state's policy vector is getting updated (I think not root state)?
        self.policy[state or root_state], value =  self.model.predict(state)#TODO nnet updates the policy and value based on this current state
        return value

    def backpropagate(value):
        reverse(self.path)
        while self.path:
            state, action = self.path.pop(0)
            self.N[state][action] += 1
            self.W[state][action] += value
            self.Q[state][action] = self.W[state][action] / self.N[state][action]
            #TODO: Do we update the policy here (probability of taking actions from state we traversed) as well?
            # if so do we compute a new policy from the N values? or do something like
            # P[state][action] = ((N-1)*P[state][action] + 1)/N  for the action we visited?
            # and for the actions we didnt do ((N-1)*P[state][action])/N
            # since P[state][action] could be due to neural net?
            #
            # or do we want to compute total N across all actions
            # then for each action update P[state][action] = N[action]/N <- i think this one
