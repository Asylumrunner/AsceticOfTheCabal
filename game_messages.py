import tcod as libtcod
import game_constants
import textwrap

# Messages are the objects handled by the text log which displays via the UI
class Message:
    def __init__(self, text, color=libtcod.white):
        self.text = text
        self.color = color

class MessageLog:
    def __init__(self):
        self.messages = []
        self.x = game_constants.message_x
        self.width = game_constants.message_width
        self.height = game_constants.message_height

    def add_message(self, message):
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            if len(self.messages) == self.height:
                del self.messages[0]
            
            self.messages.append(Message(line, message.color))