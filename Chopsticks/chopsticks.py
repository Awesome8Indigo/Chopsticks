# from math import floor
# #hands

#return pairs if both hands are less than 5, otherwise return 0 for that hand, indicating it is out.
def is_5(x, y):
    if x >= 5:
        x = 0
    if y >= 5:
        y = 0
    return [x, y]

#normalize hand by sorting
def normalize_hand(hand):
    return tuple(sorted(hand))

#check if swap is valid (same total fingers)
def is_valid_swap(hand, original):
    if hand[0] + hand[1] != original[0] + original[1]:
        return False
    return True

#remove symmetric duplicates from list of hands
def find_symmetric(groups):
    seen = set()
    clean = []
    for h in groups:
        nh = normalize_hand(h)
        if nh not in seen:
            seen.add(nh)
            clean.append(h)
    return clean

#find all possible split moves for a given hand
def find_split_moves(hand):
    out = [
    is_5(hand[0] + hand[1] - b, b)
    for b in range(hand[0] + hand[1] + 1)
    if (
        is_valid_swap(is_5(hand[0] + hand[1] - b, b), hand) and
        normalize_hand(is_5(hand[0] + hand[1] - b, b)) != normalize_hand(hand)
    )
    ]
    clean = find_symmetric(out)
    return clean

def attack_moves(player, opponent):
    attack = [
        is_5(player[i] + opponent[0], opponent[1]) if t == 0
        else is_5(opponent[0], player[i] + opponent[1])
        for i in (0, 1) for t in (0, 1)
    ]
    return find_symmetric(attack)
    
def possible_moves(p1, p2, player=0):
    #determine current player and opponent
    p = p1 if player%2 == 0 else p2
    o = p1 if player%2 == 1 else p2
    #find all possible split moves for current player, zip with opponent's hand
    if p == p1:
        splits = list(zip(find_split_moves(p), [o] * len(find_split_moves(p))))
    else:
        splits = list(zip([o] * len(find_split_moves(p)), find_split_moves(p)))
    if p == p1:
        attacks = list(zip([p] * len(attack_moves(p, o)), attack_moves(p, o)))
    else:
        attacks = list(zip(attack_moves(p, o),[p] * len(attack_moves(p, o))))
    return splits + attacks

class node:
    def __init__(self, p1, p2, player=0, parent_states=None):
        self.p1 = p1
        self.p2 = p2
        self.player = player
        self.children = []
        self.parents = []
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
        if (self.p1 == (0, 0)) or (self.p2 == (0, 0)):
            return True
        return False

def game():
    root = node((1,1), (1,1), 0)
    frontier = [root]
    terminal_paths = []

    while frontier:
        state = frontier.pop(0)  # BFS
        
        if state.is_terminal():
            terminal_paths.append(state)
            print("Terminal:", state.p1, state.p2, state.player)
            continue

        # Expand children
        state.expand()
        # Add children to frontier only if their state hasn’t been visited in this path
        for child in state.children:
            child_state_tuple = (tuple(child.p1), tuple(child.p2), child.player)
            if child_state_tuple not in state.parent_states:
                frontier.append(child)

    return terminal_paths

# a = game()

