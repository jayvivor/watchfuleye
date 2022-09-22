import utils
from player import Player
import constants

class House:

    default_rooms = {
                    "common":["Backyard","TV Room","Kitchen","Laundry Room"],
                    "bedrooms":["HoH Room","Bedroom 1","Bedroom 2","Bedroom 3", "Bedroom 4"]
    }


    def __init__(self, rooms=default_rooms, players=None):
        self.active = players if players else [Player() for _ in range(constants.default_cast_size)]
        self.evicted = []
        self.pre_jury = []
        self.jury = []
        self.hohs = []
        self.noms = []
        self.pov = []
        self.safe = []
        self.cast = {
            "active": self.active,
            "evicted":self.evicted,
            "pre-jury": self.pre_jury,
            "jury": self.jury,
            "hoh": self.hohs,
            "noms": self.noms,
            "pov": self.pov,
            "safe": self.safe  #TODO: etc etc.
        }
        self.community_knowledge = {}  #Public duos, etc.

        self.rooms = rooms

    def run_comp(self, pool):
        scoreboard = utils.Dataset(pool, Player.get_comp_score, lambda hg: hg.name)  #(player,score) tuple
        #Throwing. For now, if the player would throw, they will halve their score.
        for player in scoreboard.data_dict.keys():
            if player.would_throw(self.get_context()):
                scoreboard[player] = (utils.ranged(scoreboard[player]/2))
                print(f"{player.name} is throwing the challenge.")
        return scoreboard.sort()  #TODO: softmax it instead for some randomness.

    def get_pool(self, name):
        return self.cast[name]

    def get_context(self):
        return len(self.active)  #TODO: This is pretty much a placeholder. Determine context later.

    def evict(self, hg, jury=True):
        for group in self.cast.values():
            if hg in group:
                group.remove(hg)
        if jury:
            self.jury.append(hg)
        else:
            self.pre_jury.append(hg)
        
    