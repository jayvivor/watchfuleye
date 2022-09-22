from player import Player
from house import House
import utils
import constants
from moment import *

class Season:

    def __init__(self, name="Watchful Eye", cast_size=constants.default_cast_size, narrator=None):
        self.narrator = narrator if narrator else Narrator()
        self.cast = [Player() for _ in range(cast_size)]
        self.house = House(self.cast)
        self.name = name
        self.cycles = [Cycle() for _ in range(cast_size - 2)] + [Cycle("Finale")]
    
    def run_cycle(self, index):
        cycle = self.cycles[index]
        for day in range(cycle.num_days):
            results = cycle.run_cycle(day)
            title = results[0].upper()
            print(title)
            for r in results:
                print(self.narrator.say(r))


class Cycle:

    week = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

    event_dict = {
        "free time": 
        {
            "action": Player.free_time,
            "pool": "active",
            "title": "Free Time",
        },
        "hoh comp":
        {
            "action": House.run_comp,
            "pool": "active",
            "title": "Head of Household Competition"
        }
    }

    default_schedule =  [
                        ["hoh comp"] + ["free time"] * 9,\
                        ["free time"] * 10,\
                        ["hoh meetings"] + ["free time"] * 4 + ["nominations"] + ["free time"] * 4,\
                        ["free time"] * 10,\
                        ["free time"] * 3 + ["veto draw"] + ["free time"] + ["veto comp"] + ["free time"] * 4,\
                        ["free time"] * 10,\
                        ["veto meeting"] + ["free time"] * 4 + ["pov ceremony"] + ["free time"] * 4,\
                        ["campaign"] + ["free time"] * 8 + ["eviction"]
    ]

    def __init__(self, house=None, schedule=default_schedule):
        self.schedule = schedule
        self.house = house if house else House()
        self.num_days = len(schedule)

    def run_cycle(self):  #TODO: implementation logic
        return [self.run_day(i) for i in range(self.num_days)]
    
    def run_day(self, day_number):
        results = []  # A list of a list of moments
        for item in self.schedule[day_number]:
            pool = self.house.cast[Cycle.event_dict[item]["pool"]]
            action = Cycle.event_dict[item]["action"]
            title = Cycle.event_dict[item]["title"]
            args = Cycle.event_dict[item].get("args")
            results.append([action(p, args) if args else action(p) for p in pool])
        return title, results

class Narrations:


    def talk(participants, location):
        return f"{utils.listed([p.name for p in participants])} are having a conversation in the {location}."

    def fight(fight):
        return f"A fight broke out."


class Narrator:

    default_dialect = {
        Conversation: lambda: Narrations.talk,
        Fight: Narrations.fight
    }

    def __init__(self, dialect=None):
        if dialect:
            self.dialect = Narrator.default_dialect
            for key, val in dialect.items():
                self.dialect.update({key:val})
    
    def say(self, moment):
        return self.dialect[moment]




