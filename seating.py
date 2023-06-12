from models import Table, TableConfiguration
from rules import PreyRule, RepeatPlayersRule, RepeatPlayersPositionRule
import random
import sys


class Seating:

    def __init__(self, players):
        self.num_players = len(players)
        self.players = players
        self.num_tables_of_5, self.num_tables_of_4 = self.__calculate_table_configuration()
        self.rules = [PreyRule(), RepeatPlayersRule(), RepeatPlayersPositionRule()]

        self.minimum_found_score = sys.maxsize
        self.current_solution = None

    def __calculate_table_configuration(self):
        tables_of_5 = self.num_players // 5
        remaining_players = self.num_players % 5
        while remaining_players % 4 != 0:
            tables_of_5 -= 1
            remaining_players += 5
        tables_of_4 = remaining_players // 4

        return tables_of_5, tables_of_4

    def _create_tables(self):
        tables = []
        tables.extend([Table(5) for _ in range(self.num_tables_of_5)])
        tables.extend([Table(4) for _ in range(self.num_tables_of_4)])
        return tables

    def calc_round_score(self, tables):
        score = 0
        for rule in self.rules:
            score += rule.apply(tables)
        return score

    def calc_table_score(self, table):
        score = 0
        for rule in self.rules:
            score += rule.single_apply(table)
        return score

    def generate_round(self):
        self.minimum_found_score = sys.maxsize
        tmp_players = self.players[:]
        random.shuffle(tmp_players)
        # sorted(tmp_players, key=lambda x: len(x.players_already_met), reverse=True)
        table_configuration = TableConfiguration(self._create_tables(), self.rules)

        self._generate_round(tmp_players, table_configuration)

        return self.current_solution, self.minimum_found_score

    def _generate_round(self, remaining_players, table_configuration):
        score = table_configuration.total_score()

        if score < self.minimum_found_score:
            if table_configuration.is_completed():
                self.minimum_found_score = score
                self.current_solution = [t.clone() for t in table_configuration.tables]
                #print(f"Solution found with score {score}")

            else:
                for player in remaining_players[:]:
                    table_configuration.add_player(player)
                    remaining_players.remove(player)
                    self._generate_round(remaining_players, table_configuration)
                    table_configuration.remove_last_player()
                    remaining_players.append(player)
                    if score >= self.minimum_found_score:
                        break




