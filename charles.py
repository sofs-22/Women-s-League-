from random import choice, sample, random, uniform
from Data import teams, random_game_dates, random_game_dates_pt
from operator import attrgetter
from copy import copy
from random import sample
from datetime import datetime

class Individual:
    def __init__(self, representation=None, teams=None, repetition=False):
        self.teams = teams
        self.size = len(teams) * (len(teams) - 1)

        if representation is None:
            if repetition:
                self.representation = [[team1, team2] for team1 in teams for team2 in teams if team1 != team2]
            else:
                self.representation = []
                while len(self.representation) < self.size:
                    match = sample(teams, 2)
                    if match not in self.representation:
                        self.representation.append(match)
        else:
            self.representation = representation

        # Include random_game_dates here when calling create_game_date_mapping
        self.random_game_dates = random_game_dates_pt

        self.game_date_mapping = self.create_game_date_mapping(self.random_game_dates)
        self.fitness = self.get_fitness()

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f" Fitness: {self.fitness}"

    def create_game_date_mapping(self, random_game_dates_pt):
        game_date_mapping = {}
        for i, game in enumerate(self.representation):
            game_date_mapping[str(game)] = random_game_dates_pt[i]
        return game_date_mapping

    def get_fitness(self):
        """
            Calculate the fitness of an individual representation for the scheduling problem.

            This function evaluates the fitness of a schedule based on several hard and soft constraints.
            The higher the fitness value, the better the schedule satisfies the given constraints.

            Hard Constraints:
            1. All teams must play against each other twice (once at home and once away).
               - Penalize if any pair of teams does not meet this condition.
            2. No team should play more than two consecutive away games.
               - Penalize if a team plays more than two away games in a row.
            3. No team should play more than one game in one weekend.
               - Penalize if a team plays two games with less than a 2-day gap.

            Soft Constraints:
            1. Classic matches (e.g., Sporting vs. Benfica) should be scheduled on prime time (Saturdays).
               - Reward if a classic match is on a Saturday.
               - Penalize if a classic match is not on a Saturday.
            2. Balance the number of games played on Saturdays and Sundays for each team.
               - Reward schedules that have a balanced ratio of Saturday to Sunday games for each team.
            3. Ensure no two classic matches occur within a weekend interval, but benefit if there is a week interval.
               - Reward if there is a weekend pause between classic matches.
               - Smaller reward if classic matches have a one-week interval.

            Returns:
                int: The calculated fitness value of the individual representation.
            """
        fitness = 0
        matches = {team: [] for team in self.teams}

        # Collect matches for each team
        for game in self.representation:
            matches[game[0]].append(game)
            matches[game[1]].append(game)

        # Check if all teams play together twice (once at home and once away)
        pairs_count = {}
        for game in self.representation:
            pair = tuple(sorted(game))
            if pair not in pairs_count:
                pairs_count[pair] = 0
            pairs_count[pair] += 1

        for count in pairs_count.values():
            if count != 2:
                fitness -= 10  # Penalize for not meeting the condition

        # Check if no team plays more than two consecutive away games
        for team, games in matches.items():
            away_streak = 0
            for game in games:
                if game[1] == team:  # Away game
                    away_streak += 1
                    if away_streak > 2:
                        fitness -= 10  # Penalize for more than two consecutive away games
                else:
                    away_streak = 0


        # Check if no team plays more than once in one wekeend
        for team, games in matches.items():
            game_dates = [self.game_date_mapping[str(game)] for game in games]
            for i in range(len(game_dates) - 1):
                if abs((game_dates[i + 1] - game_dates[i]).days) < 2:
                    fitness -= 10  # Penalize for not meeting the 5-game interval condition

        # SOFT CONSTRAINTS
        # 1) Classics should be on prime time
        classics = [['Sporting', 'Benfica'], ['Benfica', 'Sporting'], ['Sporting', 'Porto'], ['Porto', 'Sporting'], ['Porto', 'Benfica'], ['Benfica', 'Porto'],]

        game_date_mapping = self.create_game_date_mapping(random_game_dates_pt)

        for match in self.representation:
            match_str = str(match)
            if match in classics:
                match_date = game_date_mapping[match_str]
                if match_date.weekday() == 5:
                    fitness += 1  # Larger reward for meeting the soft constraint
                else:
                    fitness -= -1

        # 2) Check if the ratio of Saturday games is balanced with Sunday's
        saturdays_played = {team: 0 for team in self.teams}
        sundays_played = {team: 0 for team in self.teams}

        for match in self.representation:
            match_str = str(match)
            if match in classics:
                match_date = game_date_mapping[match_str]
                if match_date.weekday() == 5:
                    saturdays_played[match[0]] += 1
                    saturdays_played[match[1]] += 1
                else:
                    sundays_played[match[0]] += 1
                    sundays_played[match[1]] += 1

        # Calculate the fitness contribution for this soft constraint
        saturday_sunday_difference = sum(abs(saturdays_played[team] - sundays_played[team]) for team in self.teams)
        saturday_sunday_fitness_contribution = min(5, 5 - saturday_sunday_difference)
        fitness += saturday_sunday_fitness_contribution

        # 3) Ensure no two classic matches occur with less than a weekend in between but benefit if a week of interval
        for i, match in enumerate(self.representation):
            if match in classics:
                match_date = self.game_date_mapping[str(match)]
                for other_match in self.representation[i + 1:]:
                    if other_match in classics:
                        other_match_date = self.game_date_mapping[str(other_match)]
                        days_interval = (other_match_date - match_date).days
                        if days_interval > 8:  # A weekend of pause between classics
                            fitness += 2
                        elif days_interval >= 7:  # classics with an interval of one week
                            fitness += 1
                        # Break loop if a classic match with enough interval is found
                        break

        return fitness


    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f"Representation: {self.representation}, Fitness: {self.fitness}"

class Population:
    def __init__(self, size, teams, elitism=False, **kwargs):
        self.size = size
        self.teams = teams
        self.elitism = elitism
        self.individuals = [Individual(teams=teams, representation=None, repetition=kwargs.get("repetition", False)) for _ in range(size)]

    def evolve(self, gens, xo_prob, mut_prob, select, mutate, crossover):
        best_fitness = None  # Initialize best_fitness variable
        fitness_list=[]

        for gen in range(gens):
            new_pop = []

            if self.elitism:
                # Apply elitism: Preserve the best individual from the current population
                best_individual = max(self.individuals, key=lambda x: x.fitness)
                new_pop.append(best_individual)

            # Apply crossover and mutation
            while len(new_pop) < self.size:
                parent1, parent2 = select(self), select(self)

                if uniform(0, 1) < xo_prob:
                    offspring1, offspring2 = crossover(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1, parent2

                if uniform(0, 1) < mut_prob:
                    offspring1 = mutate(offspring1)
                if uniform(0, 1) < mut_prob:
                    offspring2 = mutate(offspring2)

                new_pop.append(Individual(teams=self.teams, representation=offspring1.representation))
                if len(new_pop) < self.size:  # Ensure we don't exceed population size
                    new_pop.append(Individual(teams=self.teams, representation=offspring2.representation))

            self.individuals = new_pop


            # Update best_fitness if a new best solution is found
            max_fitness = max(self.individuals, key=lambda x: x.fitness).fitness
            fitness_list.append(max_fitness) # keep the fitness if the generation
            if best_fitness is None or max_fitness > best_fitness:
                best_fitness = max_fitness

            # Evaluate fitness, etc.
            print(f"Best individual of gen #{gen + 1}: {max(self.individuals, key=attrgetter('fitness'))}")

        return best_fitness, fitness_list



    def best_individual(self):
        return max(self.individuals, key=lambda x: x.fitness)

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]