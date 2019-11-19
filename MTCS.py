#dictionary of policies based on state
policy = {}
#dictionary of value function based on state
value = {}
#dicitonary of dictionaries of Q values, each dictionary is the value based on a certain action
Q = {}
#dictionary of dictionaries of number of times performed an action from a state,
# each dictionary is the value based on a certain action
N = {}
#visited states in the search tree
visited = []

def MCTS(root, game, nnet):
    #call the search on the root node
    search_helper(root, game, nnet)

def search_helper(state, game, nnet):
    if state not in visited:
        visited.append(state)
        policy[state], value[state] = nnet.predict(state)
