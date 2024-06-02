from random import randint, sample, shuffle
from Data import teams
from charles import Individual


def swap_mutation(individual):
    """Swap mutation for a scheduling problem Individual

    Args:
        individual (Individual): A scheduling problem Individual

    Returns:
        Individual: Mutated Individual
    """

    mut_indexes = sample(range(0, len(individual)), 2)
    individual[mut_indexes[0]], individual[mut_indexes[1]] = individual[mut_indexes[1]], individual[mut_indexes[0]]
    return individual

def insertion_mutation(individual):
    """Insertion mutation for a scheduling problem Individual

    Args:
        individual (Individual): A scheduling problem Individual

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(len(individual.representation)), 2)
    mut_indexes.sort()
    gene = individual.representation.pop(mut_indexes[1])
    individual.representation.insert(mut_indexes[0], gene)
    return individual

def inversion_mutation(individual):
    """Inversion mutation for a scheduling problem Individual

    Args:
        individual (Individual): A scheduling problem Individual

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(len(individual.representation)), 2)
    start, end = min(mut_indexes), max(mut_indexes)
    individual.representation[start:end] = reversed(individual.representation[start:end])

    return individual


def scramble_mutation(individual):
    """Scramble mutation for a scheduling problem Individual

    Args:
        individual (Individual): A scheduling problem Individual

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(len(individual.representation)), 2)
    start, end = min(mut_indexes), max(mut_indexes)
    subset = individual.representation[start:end]
    shuffle(subset)
    individual.representation[start:end] = subset

    return individual



def displacement_mutation(individual):
    """Displacement mutation for a scheduling problem Individual

    Args:
        individual (Individual): A scheduling problem Individual

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(len(individual.representation)), 2)
    start, end = min(mut_indexes), max(mut_indexes)
    subset = individual.representation[start:end]
    del individual.representation[start:end]
    insert_index = randint(0, len(individual.representation))
    individual.representation[insert_index:insert_index] = subset

    return individual




if __name__ == "__main__":
    test = Individual(representation=[1, 2, 3, 4], teams=teams)
    print("Before mutation:", test.representation)
    swap_mutation(test)
    print("After swap mutation:", test.representation)
    inversion_mutation(test)
    print("After inversion mutation:", test.representation)