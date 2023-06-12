from models import Player
from seating import Seating
from time import time


NUM_PLAYERS = 250


def print_round(tables, i, score, duration):
    print(f"### ROUND {i} ({score}) [{duration:.{4}f}] ###")
    return
    for table in tables:
        print([table.players[i].name for i in range(len(table.players))])


def update_players_info(tables):
    for table in tables:
        for i in range(len(table.players)):
            player = table.players[i]
            player.preys.add(table.get_prey_of(player))
            player.players_already_met.update(table.players)
            player.players_already_met.remove(player)
            player.played_positions.add(i)


if __name__ == '__main__':
    players = [Player(name=f"#{i}", id=i) for i in range(NUM_PLAYERS)]

    seating = Seating(players)

    print(f"Table configuration is {seating.num_tables_of_5} tables of 5 and {seating.num_tables_of_4} tables of 4")

    for i in range(7):
        start = time()
        round_tables, score = seating.generate_round()
        duration = time() - start
        print_round(round_tables, i, score, duration)
        if i < 3:
            update_players_info(round_tables)
