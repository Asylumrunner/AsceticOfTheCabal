""" {
    "utterance": "sup idiot",
    "choices": [
        {
            "player_utterance": "sup",
            "shop": None,
            "response": {
                "utterance": "",
                "choices": []
            }
        },
        {
            "player_utterance": "sell me some shit",
            "shop": <Shop Object>
            "response": {
                "utterance": "",
                "choices": []
            }
        }
    ]
} """

class Conversation():
    def __init__(self, start, conversation_dict):
        self.root = self.bookmark = Topic(start, conversation_dict)
    
    def respond(self, index):
        if index < len(self.bookmark.responses) and self.bookmark.responses[index].shop == None:
            self.bookmark = self.bookmark.responses[index]
        elif index < len(self.bookmark.responses):
            return self.bookmark.responses[index].shop
        return self.bookmark
    
    def reset(self):
        self.bookmark = self.root

class Topic():
    def __init__(self, utterance, conversation_dict, shop=None):
        self.utterance = conversation_dict[str(utterance)]['utterance']
        self.shop = shop
        self.choices = [value for key, value in conversation_dict[str(utterance)].items() if 'choice' in key and value != '']
        self.responses = [Topic(value, conversation_dict) for key, value in conversation_dict[str(utterance)].items() if 'goto' in key and value != '']
