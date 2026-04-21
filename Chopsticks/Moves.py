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
