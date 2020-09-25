import random
import locale
#class for player

class Player(object):

    def __init__(self,name, money, health = 100):
        '''
        Creates in instance of the player and sets the amount of health and money they start the game with
        :param money: int
        :param health: int
        '''
        self.name = name
        self.money = money
        self.health = health
        self.inventory = {"Weed": 0, "Coke": 0, "Heroin": 0, "Acid": 0, "Meth": 0, "Hash": 0}
        self.count = 1


    def __str__(self):
        '''
        returns a string of the players name current money available and current health
        :return: string
        '''

        return str(self.name)+" "+str(self.money)

    def add_player_inventory(self, drug, quantity):
        """
        Adds new drugs and there quantity to the dictionary of players inventory.
        :param drug: string
        :param quantity: int
        :return: none
        """
        if drug not in self.inventory:
            self.inventory[drug] = quantity
        else:
            self.inventory[drug] += quantity
        print(str(self.inventory))

    def remove_player_inventory(self, drug, quantity):
        """
        removes the quatity of drug just sold from the players iniventory.
        :param drug: string
        :param quantity: int
        :return: none
        """
        self.inventory[drug] -= quantity

    def remove_player_money(self, money):
        """
        reduces the players money by the amount spent on a product sale.
        :param money: int (amount to be removed from player.money)
        :return: none
        """

        self.money -= money


    def add_player_money(self, money):
        """
        updates the players money with the value of the sale.
        :param money: int
        :return: none
        """

        self.money += money

    def is_sell_deal_valid(self, drug, quantity):
        """
        checks to see if the player has the right drug and amount in there invetory to make the sell deal
        and returns true or false depending on the outcome of the check.
        :param drug: drug instance
        :param quantity: int
        :return: bohleon
        """
        if drug in self.inventory:
            if quantity <= self.inventory[drug]:
                return True
        return False

#Class for traded drugs in the game
class Drugs(object):

    def __init__ (self,name, value, _valueHighBound, _valueLowBound, quantity):
        '''
        creates an instance of a drug used in the game setting up the name, the starting value per drug unit,
        the low and high boundry for the value of a drug unit and the starting quantity of the drug that will
        be avialible
        :param name: string (user input)
        :param value: int
        :param _valueHighBound: int
        :param _valueLowBound: int
        :param quantity: random int
        '''

        self.name = name
        self.value = value
        self.quantity = quantity
        self.highbound = _valueHighBound
        self.lowbound = _valueLowBound
        self.price_paid = 0

    def __str__(self):
        # returns a string with the name and value of the instance

        return str(self.name)+"  "+str(self.value)+"   "+str(self.quantity)

    def __set__(self):
        '''
        sets the price and quanttiy for a new month
        '''
        self.value = random.randint(self.lowbound, self.highbound)
        self.quantity = random.randint(10, 250)

    def isbuydealvalid(self, playerCash, quantity):
        '''
        checks to see if the player has enough cash to make the deal and there are enough drugs to make the deal

        returns: a bohleon
        '''

        if self.quantity >= quantity:
            if quantity*self.value <= playerCash:
                return True

        return False

    def updateQuantity(self, quantity):
        # updates the quantity of drugs aviliable

        self.quantity -= quantity

    def update_price_paid(self, price):
        """

        :param price:
        :return:
        """
        self.price_paid = price


def make_buy_deal(quantity, drug, drugs, player):
    """
    checks to see if the player is making a valid deal and if it is updates the players inventory,
    money and price paid then removes the purchased quantity from the avialble amount.
    quanttity = int
    drug = string
    drugs = dict
    player = player instance
    """

    value = quantity * drugs[drug].value

    if drugs[drug].isbuydealvalid(player.money, quantity) == True:

        player.add_player_inventory(drug, quantity)
        drugs[drug].updateQuantity(quantity)
        player.remove_player_money(value)

        return True
    else:

        return False

def make_sell_deal(quantity, drug, drugs, player):
    """
    checks to see if the sell deal is valid and then updates the players inventory and money acordingly.
    quanttity = int
    drug = string
    drugs = dict
    player = player instance
    """

    value = drugs[drug].value * quantity

    if player.is_sell_deal_valid(drug, quantity) == True:

        player.add_player_money(value)
        player.remove_player_inventory(drug, quantity)

def average_price_paid(price1, price2, quan1, quan2, drug, drugs):
    """
    works out the average price paid of two different deals with different prices and quantitys then updates
    the price paid for that instance of drug
    :return:int
    """
    print(price1)
    print(price2)
    print(quan1)
    print(quan2)

    av = (quan1*price1)+(quan2*price2)
    avs = av/(quan2+quan1)

    drugs[drug].update_price_paid(avs)

    return round(avs)


def set_new_month(drugs, player):
    """
    sets the drug prince and quantity for a new month then increase the count by 1.
    when count reaches 21 it calls the end of game function
    :param drugs:
    :return:
    """
    for i in drugs:
        drugs[i].__set__()

    player.count += 1
