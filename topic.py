

""" {
    "utterance": "sup idiot",
    "choices": [
        {
            "player_utterance": "sup",
            "response": {
                "utterance": "",
                "choices": []
            }
        },
        {
            "player_utterance": "no",
            "response": {
                "utterance": "",
                "choices": []
            }
        }
    ]
} """

class Conversation():
    def __init__(self, conversation_dict):
        self.root = self.bookmark = Topic(conversation_dict['utterance'], conversation_dict['choices'])
    
    def respond(self, index):
        if index < len(self.bookmark.responses):
            self.bookmark = self.bookmark.responses[index]
        return self.bookmark

class Topic():
    def __init__(self, utterance, choices=None):
        self.utterance = utterance
        self.choices = [choice["player_utterance"] for choice in choices]
        self.responses = [Topic(choice["response"]["utterance"], choice["response"]["choices"]) for choice in choices]
