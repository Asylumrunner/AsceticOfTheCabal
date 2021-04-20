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
    def __init__(self, conversation_dict):
        self.root = self.bookmark = Topic(conversation_dict['utterance'], None, conversation_dict['choices'])
    
    def respond(self, index):
        if index < len(self.bookmark.responses) and self.bookmark.responses[index].shop == None:
            self.bookmark = self.bookmark.responses[index]
        elif index < len(self.bookmark.responses):
            return self.bookmark.responses[index].shop
        return self.bookmark
    
    def reset(self):
        self.bookmark = self.root

class Topic():
    def __init__(self, utterance, shop=None, choices=None):
        self.utterance = utterance
        self.shop = shop
        self.choices = [choice["player_utterance"] for choice in choices]
        self.responses = [Topic(choice["response"]["utterance"], None, choice["response"]["choices"]) for choice in choices]
