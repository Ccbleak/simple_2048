class StateMachine:
    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []

    def add_state(self, name, handler, end_state=False):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)
            
    def set_start(self, name):
        self.startState = name.upper()
        
    def run(self, cargo):
        handler = self.handlers[self.startState]  # start from start state
        while True:
            newState, cargo = handler(cargo)  # turn to new state
            if newState.upper() in self.endStates:  # end state
                print("Reached", newState)
                break
            else: # change the handler function
                handler = self.handlers[newState.upper()]