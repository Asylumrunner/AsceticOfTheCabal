# Fluids are inert, intangible entities that sit on the ground and can be passed through
# potentially inflicting a status effect upon the thing that goes through it
# ex. Blood, Poison Goop, Water
class Fluid():
    def __init__(self, conductive=True, statuses=[], time=0):
        self.conductive = conductive
        self.statuses = statuses
        self.time = time

    def inflict_statuses(self, entity):
        for status in self.statuses:
            entity.get_component("StatusContainer").inflict_status(status, time)
