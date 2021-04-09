from topic import Conversation

# Character describes an NPC that can be talked to, and contains their physical description, their Conversation, and a portrait for use in the UI
class Character():
    def __init__(self, description, conv_options, portrait=None):
        self.description = description
        self.conv_options = Conversation(conv_options)
        self.portrait = portrait

    # Return the conversation node that the player is currently at (the start, if they've never spoken)
    def get_conversation(self):
        return self.conv_options.bookmark
    
    # Progress the conversation forward with a dialogue option
    def talk(self, response_index=None):
        if response_index is not None:
            return self.conv_options.respond(response_index)
        else:
            return self.conv_options.bookmark