class Action: 
    def __init__(self,Name,Dependencies):
        self.Dependencies = Dependencies
class Goal(Action): pass