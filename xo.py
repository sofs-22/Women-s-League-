from random import randint, sample, uniform, random, choice
from charles import Individual
from copy import copy

def single_point_xo(parent1, parent2):
    """Implementation of single point crossover.

    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.



    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    xo_point = randint(1, len(parent1.representation) - 1)

    offspring1_repr = parent1.representation[:xo_point] + parent2.representation[xo_point:]
    offspring2_repr = parent2.representation[:xo_point] + parent1.representation[xo_point:]

    offspring1 = Individual(teams=parent1.teams, representation=offspring1_repr)
    offspring2 = Individual(teams=parent2.teams, representation=offspring2_repr)

    return offspring1, offspring2

def cycle_xo(parent1, parent2):
    """Implementation of cycle crossover.

    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.

    Returns:
        tuple: Two offspring, resulting from the crossover.
    """
    size = len(parent1.representation)
    offspring1 = [None] * size
    offspring2 = [None] * size

    while None in offspring1:
        index = offspring1.index(None)
        val1 = parent1.representation[index]
        val2 = parent2.representation[index]

        # copy the cycle elements
        while val1 != val2:
            offspring1[index] = parent1.representation[index]
            offspring2[index] = parent2.representation[index]
            val2 = parent2.representation[index]
            index = parent1.representation.index(val2)

        # copy the rest
        for i in range(size):
            if offspring1[i] is None:
                offspring1[i] = parent2.representation[i]
                offspring2[i] = parent1.representation[i]

    return Individual(representation=offspring1, teams=parent1.teams), Individual(representation=offspring2, teams=parent1.teams)


def pmx(parent1, parent2):
    """Implementation of partially matched/mapped crossover.

    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.

    Returns:
        tuple: Two offspring, resulting from the crossover.
    """
    size = len(parent1.representation)
    xo_points = sample(range(size), 2)
    xo_points.sort()

    def pmx_offspring(x, y):
        o = [None] * size
        o[xo_points[0]:xo_points[1]] = x.representation[xo_points[0]:xo_points[1]]
        z = set(y.representation[xo_points[0]:xo_points[1]]) - set(x.representation[xo_points[0]:xo_points[1]])

        # numbers that exist in the segment
        for i in z:
            temp = i
            index = y.representation.index(x.representation[y.representation.index(temp)])
            while o[index] is not None:
                temp = index
                index = y.representation.index(x.representation[temp])
            o[index] = i

        # numbers that don't exist in the segment
        while None in o:
            index = o.index(None)
            o[index] = y.representation[index]
        return o

    o1_rep, o2_rep = pmx_offspring(parent1, parent2), pmx_offspring(parent2, parent1)
    return Individual(representation=o1_rep, teams=parent1.teams), Individual(representation=o2_rep, teams=parent1.teams)

def geo_xo(parent1, parent2):
    size = len(parent1.representation)
    o1_rep = [None] * size
    o2_rep = [None] * size
    for i in range(size):
        r = random()
        if i < len(parent1.representation) and i < len(parent2.representation):
            o1_rep[i] = parent1.representation[i] if r < 0.5 else parent2.representation[i]
            o2_rep[i] = parent2.representation[i] if r < 0.5 else parent1.representation[i]
        elif i < len(parent1.representation):
            o1_rep[i] = parent1.representation[i]
            o2_rep[i] = parent1.representation[i]
        elif i < len(parent2.representation):
            o1_rep[i] = parent2.representation[i]
            o2_rep[i] = parent2.representation[i]
    offspring1 = Individual(teams=parent1.teams, representation=o1_rep)
    offspring2 = Individual(teams=parent2.teams, representation=o2_rep)
    return offspring1, offspring2


def uniform_xo(parent1, parent2):
    """Uniform crossover implementation.

    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.

    Returns:
        tuple: Two offspring, resulting from the crossover.
    """
    offspring1_repr = []
    offspring2_repr = []
    for gene1, gene2 in zip(parent1.representation, parent2.representation):
        if choice([True, False]):
            offspring1_repr.append(gene1)
            offspring2_repr.append(gene2)
        else:
            offspring1_repr.append(gene2)
            offspring2_repr.append(gene1)
    offspring1 = Individual(teams=parent1.teams, representation=offspring1_repr)
    offspring2 = Individual(teams=parent2.teams, representation=offspring2_repr)
    return offspring1, offspring2


def two_point_xo(parent1, parent2):
    # Select two random crossover points
    point1 = randint(0, len(parent1) - 1)
    point2 = randint(0, len(parent1) - 1)

    # Ensure point1 is before point2
    if point1 > point2:
        point1, point2 = point2, point1

    # Perform crossover
    offspring1 = copy(parent1)
    offspring2 = copy(parent2)
    offspring1[point1:point2], offspring2[point1:point2] = offspring2[point1:point2], offspring1[point1:point2]

    return offspring1, offspring2


def position_based_xo(parent1, parent2):
    """Implementation of Position-based Crossover (POS).

    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.

    Returns:
        tuple: Two offspring resulting from the crossover.
    """
    size = len(parent1.representation)
    point1, point2 = sorted(sample(range(size), 2))

    offspring1_repr = [None] * size
    offspring2_repr = [None] * size

    # Swap genes between parents at the selected points
    offspring1_repr[point1:point2] = parent2.representation[point1:point2]
    offspring2_repr[point1:point2] = parent1.representation[point1:point2]

    # Fill in the remaining positions with genes from the other parent
    # Ensure that each gene appears only once in each offspring
    idx1 = idx2 = point2
    for i in range(size):
        if offspring1_repr[i] is None:
            while parent1.representation[idx1] in offspring1_repr[point1:point2]:
                idx1 = (idx1 + 1) % size
            offspring1_repr[i] = parent1.representation[idx1]
            idx1 = (idx1 + 1) % size
        if offspring2_repr[i] is None:
            while parent2.representation[idx2] in offspring2_repr[point1:point2]:
                idx2 = (idx2 + 1) % size
            offspring2_repr[i] = parent2.representation[idx2]
            idx2 = (idx2 + 1) % size

    offspring1 = Individual(teams=parent1.teams, representation=offspring1_repr)
    offspring2 = Individual(teams=parent2.teams, representation=offspring2_repr)
    return offspring1, offspring2

def order_xo(parent1, parent2): # bad fitness
    size = len(parent1.representation)
    point1, point2 = sorted(sample(range(size), 2))

    offspring1_repr = [None] * size
    offspring2_repr = [None] * size

    offspring1_repr[point1:point2] = parent1.representation[point1:point2]
    offspring2_repr[point1:point2] = parent2.representation[point1:point2]

    def fill_offspring(offspring, parent):
        pos = point2
        for i in range(size):
            gene = parent.representation[(point2 + i) % size]
            if gene not in offspring:
                offspring[pos % size] = gene
                pos += 1

    fill_offspring(offspring1_repr, parent2)
    fill_offspring(offspring2_repr, parent1)

    offspring1 = Individual(teams=parent1.teams, representation=offspring1_repr)
    offspring2 = Individual(teams=parent2.teams, representation=offspring2_repr)
    return offspring1, offspring2



def subtour_xo(parent1, parent2):   # good fitness chega ao 7
    size = len(parent1.representation)
    offspring1_repr = [None] * size
    offspring2_repr = [None] * size

    start = randint(0, size - 1)
    end = randint(0, size - 1)
    if start > end:
        start, end = end, start

    offspring1_repr[start:end] = parent1.representation[start:end]
    offspring2_repr[start:end] = parent2.representation[start:end]

    def fill_offspring(offspring, parent, start, end):
        pos = end
        for i in range(size):
            gene = parent.representation[(end + i) % size]
            if gene not in offspring:
                offspring[pos % size] = gene
                pos += 1

    fill_offspring(offspring1_repr, parent2, start, end)
    fill_offspring(offspring2_repr, parent1, start, end)

    offspring1 = Individual(teams=parent1.teams, representation=offspring1_repr)
    offspring2 = Individual(teams=parent2.teams, representation=offspring2_repr)
    return offspring1, offspring2


def modified_order_xo(parent1, parent2): # not great fitness
    size = len(parent1.representation)
    point1, point2 = sorted(sample(range(size), 2))

    offspring1_repr = [None] * size
    offspring2_repr = [None] * size

    offspring1_repr[point1:point2] = parent1.representation[point1:point2]
    offspring2_repr[point1:point2] = parent2.representation[point1:point2]

    def fill_offspring(offspring, parent, start, end):
        pos = end
        for i in range(size):
            gene = parent.representation[(end + i) % size]
            if gene not in offspring:
                offspring[pos % size] = gene
                pos += 1

    fill_offspring(offspring1_repr, parent2, point1, point2)
    fill_offspring(offspring2_repr, parent1, point1, point2)

    offspring1 = Individual(teams=parent1.teams, representation=offspring1_repr)
    offspring2 = Individual(teams=parent2.teams, representation=offspring2_repr)
    return offspring1, offspring2









