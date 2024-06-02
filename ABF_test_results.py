import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Data import pt_teams, random_game_dates_pt
from charles import Population
from mutation import swap_mutation, insertion_mutation, inversion_mutation, scramble_mutation, displacement_mutation
from selection import rank_selection, fps, tournament_sel
from xo import modified_order_xo, subtour_xo, order_xo, position_based_xo, two_point_xo, uniform_xo, geo_xo, cycle_xo, \
    single_point_xo


def run_evolutionary_algorithm(selection_func, crossover_func, mutation_func, elitism):
    P = Population(size=50, optim="max", teams=pt_teams, sol_size=len(random_game_dates_pt),
                   valid_set=pt_teams, repetition=False, elitism=elitism)

    best_fitness, fitness_list = P.evolve(gens=200, xo_prob=0.9, mut_prob=0.2, select=selection_func,
                                          mutate=mutation_func, crossover=crossover_func)

    return best_fitness, fitness_list


selection_functions = [fps, rank_selection, tournament_sel]
crossover_functions = [single_point_xo, cycle_xo, two_point_xo, geo_xo, uniform_xo, position_based_xo, order_xo, subtour_xo, modified_order_xo]
mutation_functions = [swap_mutation, inversion_mutation, insertion_mutation, scramble_mutation, displacement_mutation]
elitism_options = [True, False]
results = []
num_runs = 30

for elitism in elitism_options:
    for selection_func in selection_functions:
        for crossover_func in crossover_functions:
            for mutation_func in mutation_functions:
                print(f"Elitism: {elitism}, Selection: {selection_func.__name__}, Crossover: {crossover_func.__name__}, Mutation: {mutation_func.__name__}")
                fitness_across_runs = []
                for _ in range(num_runs):
                    _, fitness_list = run_evolutionary_algorithm(selection_func, crossover_func, mutation_func, elitism)
                    fitness_across_runs.append(fitness_list)
                avg_fitness = np.mean(fitness_across_runs, axis=0)
                std_dev_fitness = np.std(fitness_across_runs, axis=0)
                results.append({
                    'elitism': elitism,
                    'selection_func': selection_func.__name__,
                    'crossover_func': crossover_func.__name__,
                    'mutation_func': mutation_func.__name__,
                    'avg_fitness': avg_fitness,
                    'std_dev_fitness': std_dev_fitness
                })

# Convert results to a DataFrame
df = pd.DataFrame(results)

df.to_excel('fitness_data.xlsx', index=False)


# Function to plot fitness over generations
def plot_fitness(df, group_by, title):
    grouped = df.groupby(group_by)
    plt.figure(figsize=(12, 8))
    for name, group in grouped:
        generations = np.arange(len(group.iloc[0]['avg_fitness']))
        avg_fitness = np.mean(np.vstack(group['avg_fitness']), axis=0)
        std_dev = np.mean(np.vstack(group['std_dev_fitness']), axis=0)
        plt.plot(generations, avg_fitness, label=f'{name} (Mean)')
        plt.fill_between(generations, avg_fitness - std_dev, avg_fitness + std_dev, alpha=0.2)

    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.title(title)
    plt.legend()
    plt.show()


# Plot aggregated by selection methods
plot_fitness(df, 'selection_func', 'Fitness Over Generations Aggregated by Selection Methods')

# Plot aggregated by crossover functions
plot_fitness(df, 'crossover_func', 'Fitness Over Generations Aggregated by Crossover Functions')

# Plot aggregated by mutation functions
plot_fitness(df, 'mutation_func', 'Fitness Over Generations Aggregated by Mutation Functions')
