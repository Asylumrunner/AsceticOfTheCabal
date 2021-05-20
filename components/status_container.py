from enum import Enum
class StatusEffects(Enum):
    poisoned = 1
    asleep = 2
    bleeding = 3

# A generic class designed to keep track of any number of status effects that might befall a character

class StatusContainer:
    def __init__(self):
        self.status_bools = {}
        for status in StatusEffects:
            self.status_bools[status.name] = False
        
        self.status_clocks = {}

    # Returns a list of every status currently active. Used to render status names on UI
    def get_statuses(self):
        return [status for status in self.status_bools if self.status_bools[status]]
    
    #sets a status as true. If clock is given, will set a timer for it in status_clocks
    def inflict_status(self, status_name, clock=0):
        self.status_bools[status_name] = True

        if clock != 0 and status_name in self.status_clocks:
            self.status_clocks[status_name] += clock
        elif clock != 0:
            self.status_clocks[status_name] = clock
    
    #returns if the passed status is currently true or false
    def check_status(self, status_name):
        return self.status_bools[status_name]
    
    #sets a status to false. Tick_clocks will handle any clocks associated with it
    def cure_status(self, status_name):
        self.status_bools[status_name] = False

    #Every action, ticks each clock down by 1, removing any clocks that hit 0 or are for statuses already cured
    #NOTE: I get the feeling this will bite me in the ass later. tick_clocks needs to happen before any every-turn statuses
    #like poison or bleed
    def tick_clocks(self):
        statuses_to_clear = []
        for status, clock in self.status_clocks.items():
            if not self.status_bools[status]:
                statuses_to_clear.append(status)
            elif clock == 1:
                statuses_to_clear.append(status)
            else:
                self.status_clocks[status] = clock - 1
        
        for status in statuses_to_clear:
            del self.status_clocks[status]