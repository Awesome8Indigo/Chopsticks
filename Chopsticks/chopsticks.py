# from math import floor
# #hands


#define a terminal state
from Moves import possible_moves

terminal = (0,0)

class node:
    def __init__(self, p1, p2, player=0, parent_states=None):
        self.p1 = p1
        self.p2 = p2
        self.player = player
        self.children = []
        self.parents = []
        self.state = (p1, p2, player)
        # store ancestry history as set of visited states
        if parent_states is None:
            self.parent_states = set()  
        else:
            self.parent_states = set(parent_states)

        # add own state to ancestry
        self.parent_states.add((self.p1, self.p2, self.player))

    
    def expand(self):
        moves = possible_moves(self.p1, self.p2, self.player)
        for move in moves:
            if self.player % 2 == 0:
                child = node(tuple(move[0]), tuple(move[1]), self.player + 1)
            else:
                child = node(tuple(move[1]), tuple(move[0]), self.player + 1)
            child.parents.append(self)
            self.children.append(child)
            
    def is_terminal(self):
        if terminal not in self.state:
            return False
        if (self.player != self.state.index((0,0))):
            return "loss"
        if (self.p1 == terminal):
            #return parents and the winner
            return "xp2"
        elif (self.p2 == terminal):
            return "xp1"

def game():
    root = node((1,1), (1,1), 0)
    frontier = [root]
    terminal_paths = []

    while frontier:
        state = frontier.pop(0)  # BFS
        
        match(state.is_terminal()):
            case "loss":
                continue
            case "xp1":
                print("xp1")
                return state.parents
            case "xp2":
                print("xp2")
                return state.parents
            case _:
                pass
        # Expand children
        state.expand()
        # Add children to frontier only if their state hasn’t been visited in this path
        for child in state.children:
            child_state_tuple = (tuple(child.p1), tuple(child.p2), child.player)
            if child_state_tuple not in state.parent_states:
                frontier.append(child)

    return terminal_paths

game()

