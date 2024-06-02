from operator import attrgetter
from random import uniform, choice, sample, choices


def fps(population):
    """Fitness proportionate selection implementation for maximization problem.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: Selected individual.
    """
    max_fitness = max(ind.fitness for ind in population)
    total_fitness = sum(ind.fitness for ind in population)

    # Calculate selection probabilities based on fitness proportion
    selection_probabilities = [(ind.fitness / total_fitness) for ind in population]

    # Choose an individual based on selection probabilities
    selected_index = choices(range(len(population)), weights=selection_probabilities, k=1)[0]
    return population[selected_index]


def rank_selection(population):
    """Rank-based selection implementation for maximization problem.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: Selected individual.
    """
    sorted_population = sorted(population, key=attrgetter('fitness'), reverse=True)
    ranks = [i + 1 for i in range(len(sorted_population))]
    total_ranks = sum(ranks)

    # Calculate selection probabilities based on ranks
    selection_probabilities = [rank / total_ranks for rank in ranks]

    # Choose an individual based on selection probabilities
    selected_index = choices(range(len(sorted_population)), weights=selection_probabilities, k=1)[0]
    return sorted_population[selected_index]


def tournament_sel(population, tour_size=3):
    """Tournament selection implementation for maximization problem.

    Args:
        population (Population): The population we want to select from.
        tour_size (int): Size of the tournament.

    Returns:
        Individual: Selected individual.
    """
    tournament = sample(list(population), tour_size)
    return max(tournament, key=attrgetter('fitness'))