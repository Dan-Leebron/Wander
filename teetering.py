def balanceable(numbers):
    import itertools
    balance = (sum(numbers))/2
    size = range(len(numbers))
    for permutation in itertools.permutations(numbers):
        half = []
        for element in size:
            half.append(permutation[element])
            if sum(half) == balance:
                return True
    return False