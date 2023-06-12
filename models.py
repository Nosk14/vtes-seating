from dataclasses import dataclass, field
from typing import Set, List


@dataclass
class Player:
    name: str
    id: int
    preys: Set = field(default_factory=set)
    players_already_met: Set = field(default_factory=set)
    played_positions: Set = field(default_factory=set)

    def __hash__(self):
        return self.id


@dataclass
class Table:
    size: int
    players: List = field(default_factory=list)

    def get_prey_of(self, player):
        player_position = self.players.index(player)
        return self.players[(player_position + 1) % len(self.players)]

    def clone(self):
        return Table(self.size, self.players[:])


@dataclass
class TableConfiguration:
    tables: List[Table]
    rules: List
    index: int = 0
    table_scores: List = field(init=False)

    def __post_init__(self):
        self.table_scores = [0 for _ in range(len(self.tables) + 1)]

    def add_player(self, player):
        table = self.tables[self.index]
        table.players.append(player)

        self.table_scores[self.index] = self.__calc_score_for_table(table)

        if len(table.players) == table.size:
            self.index += 1

    def remove_last_player(self):
        if self.is_completed() or len(self.tables[self.index].players) == 0:
            self.table_scores[self.index] = 0
            self.index -= 1

        table = self.tables[self.index]
        table.players.pop()

    def is_completed(self):
        return self.index == len(self.tables)

    def total_score(self):
        return sum(self.table_scores)

    def __calc_score_for_table(self, table):
        score = 0
        for rule in self.rules:
            score += rule.single_apply(table)
        return score

