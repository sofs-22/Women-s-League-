from charles import Population
from mutation import swap_mutation, inversion_mutation, insertion_mutation, scramble_mutation, displacement_mutation
from selection import fps, tournament_sel, rank_selection
from xo import single_point_xo, cycle_xo, two_point_xo, geo_xo, uniform_xo, position_based_xo, order_xo, subtour_xo, modified_order_xo
from Data import teams, pt_teams, valid_set, random_game_dates, random_game_dates_pt

P = Population(size=50, optim="max", teams=pt_teams, sol_size=len(random_game_dates_pt),
               valid_set=pt_teams, repetition=False, elitism=True)

P.evolve(gens=200, xo_prob=0.9, mut_prob=0.2, select=tournament_sel,
         mutate=swap_mutation, crossover=modified_order_xo)


def generate_schedule_table(population, game_dates_mapping):
    schedule_table = []
    for individual in population.individuals:
        schedule_representation = individual.representation
        for game in schedule_representation:
            if not game_dates_mapping:  # Check if the list is empty
                break  # Exit the loop if the list is empty
            team1, team2 = game[0], game[1]
            game_date = game_dates_mapping.pop(0)  # Retrieve and remove the first element
            game_day = game_date.strftime("%A")  # Get the day of the week
            game_month = game_date.strftime("%B")  # Get the month
            game_day_of_month = game_date.strftime("%d")  # Get the day of the month
            game_time = game_date.strftime("%H:%M")  # Get the time
            schedule_table.append([team1, team2, game_day, game_month, game_day_of_month, game_time])
    return schedule_table

def generate_schedule_table_html(schedule_table):
    html = "<table border='1'>"
    html += "<tr><th>Team 1</th><th>Team 2</th><th>Day</th><th>Month</th><th>Date</th><th>Time</th></tr>"
    for game in schedule_table:
        html += "<tr>"
        html += "<td>{}</td>".format(game[0])
        html += "<td>{}</td>".format(game[1])
        html += "<td>{}</td>".format(game[2])
        html += "<td>{}</td>".format(game[3])
        html += "<td>{}</td>".format(game[4])
        html += "<td>{}</td>".format(game[5])
        html += "</tr>"
    html += "</table>"
    return html

# Generate the schedule table
schedule_table = generate_schedule_table(P, random_game_dates_pt.copy())  # Make a copy to preserve original list

# Generate the schedule table in HTML format
schedule_table_html = generate_schedule_table_html(schedule_table)

with open("schedule_table.html", "w") as f:
    f.write(schedule_table_html)

