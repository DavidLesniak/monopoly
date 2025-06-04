class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.saldo = 1500
        self.properties = []
        self.in_jail = False

    def move(self, value):
        pass

    def buy_property(self, property):
        if property.area is None and self.saldo >= property.price:
            self.saldo -= property.price
            self.properties.append(property)
            property.area = self

    def paying_rent(self):
        pass

    def bankruptcy(self):
        pass

    def go_to_jail(self):
        pass
    