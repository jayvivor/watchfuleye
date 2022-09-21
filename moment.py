class Moment:

    def __init__(self):
        pass

class Fight(Moment):

    def __init__(self, aggressor, defender, attack, defense, intensity, result, location):
        self.aggressor = aggressor
        self.defender = defender
        self.intensity = intensity
        self.result = result

class Free_Time(Moment):  #

    def __init__(self, room, members):  #room_events is a room:event_list dictionary
        self.room = room
        self.members = members

class Conversation(Moment):

    def __init__(self, participants, convo_type, delta):
        self.participants = participants
        self.convo_type = convo_type
