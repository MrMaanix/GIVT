class SharedState:
    def __init__(self):
        self._state = "default"
    
    def set_state(self, state):
        self._state = state
    
    def get_state(self):
        return self._state
