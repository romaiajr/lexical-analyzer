from lexical_token import Token

class DataToken ():

    def __init__(self, obj):
        self.ide = obj['lexema']
        self.type = obj['type']
        self.initialized = obj["initialized"]
        self.scope = obj["scope"]
        self.params = obj["params"]
        
        


