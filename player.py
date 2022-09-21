import random
import constants
import utils
from faker import Faker
from math import sqrt
from moment import *

class Player:

    f = Faker()



    gn_names = constants.gender_neutral_names

    ## STATS
    #  Physical - speed, balance, endurance, memory, puzzle, dexterity
    #  Social - charm, persuasion, stealth, temper, gamebot, x_factor
    #  Strategic - loyalty, overplay, stubbornness, stealth, reads
    stat_types = ["speed","balance","endurance","memory","puzzle","dexterity",\
                  "charm","persuasion","stealth","temper","gamebot","x_factor","y_factor",\
                  "loyalty", "overplay","stubbornness","stealth","reads"]

    ## ATTS
    #  Mood - Anxiety, Irritability
    att_types = ["anxious","pissed"]


    def __init__(self, stats=None, atts=None, name=None):
        self.stats = {st:random.randint(1,100) for st in Player.stat_types} if not stats else stats
        self.atts = {att:random.randint(1,100) for att in Player.att_types} if not atts else atts
        # self.name = Player.f.name() if not name else name
        self.name = f"{random.choice(Player.gn_names)} {Player.f.last_name()}" if not name else name
        self.relationships = {}
        self.insights = []

    def delta_att(self, attribute, delta):
        self.atts[attribute] += delta
    
    def add_relationship(self, target):
        self.relationships.update({target:Relationship(self, target)})
    
    def get_relationship(self, target):
        return self.relationships.get(target)

    def get_target_list(self, pool):  #TODO: will return a sorted list of (player, score) tuples
        criteria = lambda x: self.get_relationship(x).trust
        scoreboard = utils.Dataset(pool, criteria, lambda p: p.name).sort()
        return scoreboard
    
    def predict(self, pool, event):  #TODO: player predicts a single event in the house based on their perception
        pass

    #Physical Game
    def get_comp_score(self, comp, skill_spread=None):  #TODO: will return a score for the challenge. skill_spread is dict.
        score = sum([self.stats[skill]*skill_spread[skill] for skill in skill_spread.keys()])
        return score

    def would_throw(self, context):  #TODO: for testing purposes, this will just be a 20% chance. work on it
        return random.choice([False, False, False, False, True])

    #Social Game
    def small_talk(self, target):
        other_rel = target.get_relationship(self)
        charm = self.stats["charm"]
        bond_delta = random.gauss((charm-20)/50 + (other_rel.stats["click"]-50)/10, constants.bond_build_fuzz)
        other_rel.atts["bond"] = utils.ranged(other_rel.atts["bond"] + bond_delta)
        return Conversation([self, target], "small talk", bond_delta)

    def trash_talk(self, target, victim):
        pass

    def game_talk(self, target):
        other_rel = target.get_relationship(self)
        pers = self.stats["persuasion"]
        bond_delta = random.gauss((pers-20)/50 + (other_rel.stats["click"]-50)/10, constants.bond_build_fuzz)
        other_rel.atts["trust"] = utils.ranged(other_rel.atts["trust"] + bond_delta)
        return Conversation([self, target], "game talk", bond_delta)

    def spread_narrative(self, target, narrative_type):  #TODO: figure out how we want narratives to work. Class?
        pass

    #Strategic Game
    def read(self, target, action, positive, *action_args):  #positive means a higher value is better for the target.
        actual_value = action(target, *action_args)
        rel = self.get_relationship(target) 
        sus = constants.sus_scale*(rel.stats["sus"]-50)  # bad reads for overly or underly sus players
        fuzzed = actual_value - sus if positive else actual_value + sus
        fuzzed = utils.ranged(fuzzed)
        return fuzzed

    def position(self, pool):
        pass


class Relationship:

    ## Relationship stats
    #  click - based on x and y factors. The further the distance, the lower the click.
    #  sus - based on target stealth, owner reads, and a bit of randomness. Initial wariness
    stat_types = ["click", "sus"]

    ## Relationship Atts
    #  Trust, Bond
    att_types = ["trust","bond"]

    def __init__(self, owner, target):
        self.owner = owner
        self.target = target
        self.initialize_stats()
        self.initialize_atts()
        

    def initialize_stats(self):
        self.stats = {}

        ## specific stats

        #  click is the distance between the x and y factors
        x_delta = self.owner.stats["x_factor"] - self.target.stats["x_factor"]
        y_delta = self.owner.stats["y_factor"] - self.target.stats["y_factor"]
        self.stats["click"] = utils.ranged(100 - sqrt(x_delta**2 + y_delta**2))

        # sus is the over/underestimation of a target's danger
        reads = self.owner.stats["reads"]
        stealth = self.target.stats["stealth"]
        self.stats["sus"] = utils.ranged(random.gauss((stealth-50)*((100-reads)/100)+50, constants.read_fuzz_scale))  #unstealthy players will be unfairly targeted etc.

    def initialize_atts(self):
        # For now, atts will be a random value, scaled to the cap constant
        self.atts = {att:random.randint(0,constants.first_impression_cap) for att in Relationship.att_types}
    


class Alliance:

    deal_types = ["deal","duo","showmance","majority","core"]

    def __init__(self, founder, members, deal_type, timestamp):
        self.timestamp = timestamp
        self.founder = founder
        self.members = members
        if deal_type in Alliance.deal_types:
            self.deal_type = deal_type
        else:
            print(f"Warning: Deal type '{deal_type}' invalid. defaulting to 'Core'.")
            self.deal_type = "Core"
        self.alive = True
        self.leaked_to = []

    def meet(purpose="vote"):
        if purpose == "vote":
            #Jointly decide who to vote; players will push back depending on a number of stats/atts
            pass

class Insight:

    def __init__(self):
        pass
        


class Conspiracy(Insight):  #Alliance, but not to be confused with actual alliance class.

    def __init__(self, snitch, confidant, alliance, timestamp):
        self.snitch = snitch
        self.confidant = confidant
        self.alliance_members = alliance.members

        ## Juiciness calculation
        # Recency: if same-day, max. If day 2 to 1 cycle later, half. anything beyond, 1/4.
        days_since = timestamp.day - alliance.timestamp.day
        if days_since == 0:
            self.recency = 1
        elif days_since <= 7:
            self.recency = constants.insight_half_life
        else:
            self.recency = constants.insight_half_life/2
        
        # Confidence: how much do you believe it
        rel = self.confidant.get_relationship(self.snitch)
        trust = rel.trust
        persuasion = self.snitch.stats["persuasion"]
        gull = constants.stat_max-self.confidant.stats["stubbornness"]
        if self.snitch in self.alliance_members:
            self.confidence = utils.ranged(trust, minimum=constants.self_snitch_constant)
        else:
            self.confidence = utils.ranged((trust+persuasion)/2-(constants.stat_max-gull))

        # Surprise: TODO: really complicated and I'll deal with it later
        self.surprise = 1

        # Freshness: if it was already leaked, it will mean little now.
        if confidant in alliance.leaked_to:
            self.freshness = 0.1
        else:
            self.freshness = 1

        self.juiciness = (self.recency * self.surprise * self.freshness * self.confidence)
        
        #build/lose trust with snitch
        rel.trust = utils.ranged(rel.trust + (self.juiciness - constants.insight_trust_threshold) * constants.insight_trust_scale)



