class Player:
    def __init__(self, isComputer):
        self.isComputer = isComputer
        self.current_card
        self.hand = []
        self.possible_cards = []
    
    def press_uno(self):
        pass
    
    def use_card(self, index):
        self.current_card = self.hand[index]
        self.hand.remove(index)
    
    def get_card():
        pass

class User(Player):
    def __init__(self, isComputer):
        self.isComputer = isComputer
        
class Computer(Player):
    def __init__(self, isComputer):
        self.isComputer = isComputer
