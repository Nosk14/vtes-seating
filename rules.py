class PreyRule:
    WEIGHT = 1000

    def __init__(self):
        pass

    def single_apply(self, table):
        score = 0
        if len(table.players) != 0:
            for i in range(len(table.players) - 1):
                player = table.players[i]
                if table.players[i+1] in player.preys:
                    score += self.WEIGHT
            if table.players[-1] and table.players[0] in table.players[-1].preys:
                score += self.WEIGHT

        return score

class RepeatPlayersRule:
    WEIGHT = 1

    def __init__(self):
        pass

    def single_apply(self, table):
        score = 0
        for player in table.players:
            score += self.WEIGHT * len(player.players_already_met.intersection(table.players))
        return score

class RepeatPlayersPositionRule:
    WEIGHT = 3

    def __init__(self):
        pass

    def single_apply(self, table):
        score = 0
        for i in range(len(table.players)):
            if i in table.players[i].played_positions:
                score += self.WEIGHT
        return score