from topic import Conversation

class Character():
    def __init__(self, description, conv_options, portrait=None):
        self.description = description
        self.conv_options = Conversation(conv_options)
        self.portrait = portrait

    def get_conversation(self):
        return self.conv_options.bookmark
    
    def talk(self, response_index=None):
        if response_index is not None:
            return self.conv_options.respond(response_index)
        else:
            return self.conv_options.bookmark