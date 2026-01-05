from chopsticks import find_split_moves

def test_find_split_moves():
    s = [[i, j] for i in range(5) for j in range(5)]
    for x in s:
        results = find_split_moves(x)
        target = sum(results[0])
        for i, lst in enumerate(results):
            assert sum(lst) == target, f"Failed on input {x}, output {results}"

test_find_split_moves()