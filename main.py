import PySimpleGUI as sg
import random
import csv
import locale


locale.setlocale(locale.LC_ALL, "")



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
    works out the average price paid for two different deals with different prices and quantitys then updates
    the price paid for that instance of drug
    :return:int
    """

    price_quants = (quan1*price1)+(quan2*price2)
    price_avg = price_quants/(quan2+quan1)

    drugs[drug].update_price_paid(price_avg)

    return round(price_avg)


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


weed = Drugs("Weed", 36, 60, 5, quantity=random.randint(1, 150))
coke = Drugs("Coke", 3745, 30000, 2500, quantity=random.randint(1, 150))
heroin = Drugs("Heroin", 1892, 9000, 1000, quantity=random.randint(1, 150))
acid = Drugs("Acid", 67, 80, 10, quantity=random.randint(1, 150))
meth = Drugs("Meth", 376, 1000, 70, quantity=random.randint(1, 150))
hash = Drugs("Hash", 12, 40, 5, quantity=random.randint(1, 150))

player = Player("", 1000, 100)

# a dictionary where the keys are a string of the drug instance name.
# used to convert user input into a usable way to call instance methods
drugs = {"Weed":weed, "Coke":coke, "Heroin":heroin, "Acid":acid, "Meth":meth, "Hash":hash}
init_cost = 0

def text_temp(text, key=None):
    """
    returns a text element of the text input variable using the specified settings.
    :param text: string
    :return: sg.Text element
    """
    return sg.Text(text, justification='center', size=(10, 2), key=key, font=('Courier', 12, "bold"))

def update_scoreboard(file, game):
    """
    opens the csv file where the top 5 scores are stored and adds the players score to it then sorts the scores
    in decending order and returns the new top 5list of dictionarys
    :return:list of dictionarys
    """

    with open(file, "r" )as top:
        scores = csv.DictReader(top)

        top_5 = list(scores)
        for i in top_5:
            i["score"] = int(i["score"])

        top_5.append(game)

        result = sorted(top_5, key=lambda i: i['score'], reverse=True)

        return result[:5]

def save_scoreboard(file, scores):
    """
    saves the updated scores dictionary back to the csv file
    :return:
    """
    csv_columns = ["score", "name"]
    with open(file, "w") as top:
        writer = csv.DictWriter(top, fieldnames=csv_columns)
        writer.writeheader()
        for data in scores:
            writer.writerow(data)
    print(scores)

def name_entry_win():
    """

    :return:
    """
    layout = [[sg.Text("DopeWars", justification='center', size=(100, 1), font=('Courier', 50, "underline"))],
              [sg.Text(size=(1, 4))],
              [sg.Text("Enter your name", justification="center", size=(80, 1), font=("Courier", 15, "bold"))],
              [sg.Text(size=(26, 1)),
              sg.In(key="name")],
              [sg.Text(size=(1, 1))],
              [sg.Text(size=(44, 1)),
              sg.Button("Ok", size=(5, 1))]]

    window = sg.Window("DopeWars", layout, size=(800, 600))

    while True:
        event, values = window.read()

        if event ==  sg.WINDOW_CLOSED:
            break

        if event == "Ok":
            player.name = values["name"]
            main_win()
            break

    window.close()


def main_win():
    drugs_column = [[sg.Text("\nInventory",justification="center", size=(10, 3), font=('Courier', 13, "bold"))],
                [text_temp("Weed")],
                [text_temp("Coke")],
                [text_temp("Heroin")],
                [text_temp("Acid")],
                [text_temp("Meth")],
                [text_temp("Hash")]]

    quantity_column = [[sg.Text("\nAmount",justification="center", size=(10, 3), font=('Courier', 13, "bold"))],
                   [text_temp(str(player.inventory["Weed"]), "Weed")],
                   [text_temp(str(player.inventory["Coke"]), "Coke")],
                   [text_temp(str(player.inventory["Heroin"]), "Heroin")],
                   [text_temp(str(player.inventory["Acid"]), "Acid")],
                   [text_temp(str(player.inventory["Meth"]), "Meth")],
                   [text_temp(str(player.inventory["Hash"]), "Hash")]]

    price_paid_column = [[sg.Text("\nPrice Paid",justification="center", size=(10, 3), font=('Courier', 13, "bold"))],
                     [text_temp(locale.currency(weed.price_paid, grouping=True), "Weedp")],
                     [text_temp(locale.currency(coke.price_paid, grouping=True), "Cokep")],
                     [text_temp(locale.currency(heroin.price_paid, grouping=True), "Heroinp")],
                     [text_temp(locale.currency(acid.price_paid, grouping=True), "Acidp")],
                     [text_temp(locale.currency(meth.price_paid, grouping=True), "Methp")],
                     [text_temp(locale.currency(hash.price_paid, grouping=True), "Hashp")]]

    product_column = [[sg.Text("\nProduct",justification="center", size=(10, 3), font=('Courier', 13, "bold"))],
                [text_temp("Weed")],
                [text_temp("Coke")],
                [text_temp("Heroin")],
                [text_temp("Acid")],
                [text_temp("Meth")],
                [text_temp("Hash")]]

    available_column = [[sg.Text("\nAvailable",justification="center", size=(10, 3), font=('Courier', 13, "bold"))],
                   [text_temp(str(weed.quantity), "Weed_")],
                   [text_temp(str(coke.quantity), "Coke_")],
                   [text_temp(str(heroin.quantity), "Heroin_")],
                   [text_temp(str(acid.quantity), "Acid_")],
                   [text_temp(str(meth.quantity), "Meth_")],
                   [text_temp(str(hash.quantity), "Hash_")]]

    cost_column = [[sg.Text("\nCost",justification="center", size=(10, 3), font=('Courier', 13, "bold"))],
                [text_temp(locale.currency(weed.value, grouping=True), "Weed__")],
                [text_temp(locale.currency(coke.value, grouping=True), "Coke__")],
                [text_temp(locale.currency(heroin.value, grouping=True), "Heroin__")],
                [text_temp(locale.currency(acid.value, grouping=True), "Acid__")],
                [text_temp(locale.currency(meth.value, grouping=True), "Meth__")],
                [text_temp(locale.currency(hash.value, grouping=True), "Hash__")]]



    cash_amount_column = [[sg.Text("\nCash:", justification="right", size=(20, 3), font=('Courier', 13, "bold")),
                       sg.Text("\n"+locale.currency(player.money, grouping=True), justification="right", size=(13, 3), font=('Courier', 13, "bold"), key="player cash"),
                       sg.Text("", size=(7, 3)),
                       sg.Combo(["Weed", "Coke", "Heroin", "Acid", "Meth", "Hash"], size=(9, 3), key="product", enable_events=True),
                       sg.Text("", size=(3, 3)),
                       sg.In(size=(8, 3), key="quantity", enable_events=True),
                       sg.Text("\n"+locale.currency(init_cost, grouping=True), key="cost", justification="right", size=(13, 3), font=('Courier', 13, "bold"))
                       ]]


    buy_sell_buttons = [[sg.Text("\nTurn:", justification="right", size=(20, 3), font=('Courier', 13, "bold")),
                     sg.Text("\n"+str(player.count)+"/15", justification="right", size=(10, 3), font=('Courier', 13, "bold"), key="count"),
                     sg.Text(size=(7, 1)),
                     sg.Button("Buy", size=(10, 2)),
                     sg.Text(size=(2, 1)),
                     sg.Button("Sell", size=(10, 2)),
                     sg.Text(size=(2, 1)),
                     sg.Button("End Turn", size=(10, 2))]]

    layout = [[sg.Text("DopeWars", justification='center', size=(100, 1), font=('Courier', 50, "underline"))],
          [sg.Column(drugs_column, size=(115, 330)),
           sg.Column(quantity_column, size=(115, 330)),
           sg.Column(price_paid_column, size=(125, 320)),
           sg.VSeparator(),
           sg.Column(product_column, size=(115, 330)),
           sg.Column(available_column, size=(115, 330)),
           sg.Column(cost_column, size=(115, 330))],
           [sg.Text("")],
           [sg.Column(cash_amount_column, size=(900, 50))],
           [sg.Column(buy_sell_buttons, size=(800, 75))]
          ]


    window = sg.Window("DopeWars", layout, size=(800, 600))

    while True:
        event, values = window.read()

        product = values["product"]

        cost = window["cost"]
        try:
            if cost != drugs[product].value * int(values["quantity"]):
                window["cost"].update("\n"+locale.currency(drugs[values["product"]].value * int(values["quantity"]), grouping=True))

        except:
            window["cost"].update("\n"+locale.currency(init_cost, grouping=True))

        if event ==  sg.WINDOW_CLOSED:
            break

        if event == "Buy":

            price2 = drugs[values["product"]].price_paid

            quan2 = player.inventory[values["product"]]
            try:

                if make_buy_deal(int(values["quantity"]), values["product"], drugs, player) == True:
                    #updates the product shown in the players inventory
                    window[values["product"]].update(str(player.inventory[values["product"]]))
                    #updates the amount of product shown available to buy
                    window[values["product"]+"_"].update(drugs[values["product"]].quantity)
                    #updates the players available cash shown
                    window["player cash"].update("\n"+locale.currency(player.money, grouping=True))
                    #updates the price paid column shown
                    window[values["product"]+"p"].update(locale.currency(average_price_paid(drugs[values["product"]].value,
                                                                       price2,
                                                                       int(values["quantity"]),
                                                                       quan2,
                                                                       values["product"],
                                                                       drugs), grouping=True))

            except:

                pass

        if event == "Sell":
            try:
                make_sell_deal(int(values["quantity"]), values["product"], drugs, player)
                # updates the product in the players inventory
                window[values["product"]].update(str(player.inventory[values["product"]]))
                # updates the amount of product available to buy
                window[values["product"] + "_"].update(drugs[values["product"]].quantity)
                # updates the players available cash
                window["player cash"].update("\n" + locale.currency(player.money, grouping=True))
                if player.inventory[values["product"]] == 0:
                    window[values["product"] + "p"].update(locale.currency(0, grouping=True))

            except:
                pass


        if event == "End Turn":
            set_new_month(drugs, player)
            #updates the turn counter
            if player.count != 16:
                window["count"].update("\n"+str(player.count)+"/15")
                # updates the amount of products available to buy and there cost
                for i in drugs:
                    window[i+"_"].update(drugs[i].quantity)
                    window[i+"__"].update(locale.currency(drugs[i].value, grouping=True))

            else:
                highscores_win()
                break



    window.close()

def highscores_win():
    """

    :return:
    """
    result = {"score": (player.money), "name": player.name}

    file = "top_five_scores.csv"

    scores = update_scoreboard(file, result)

    save_scoreboard(file, scores)

    numbers_column = [[sg.Text("\nPos",justification="center", size=(10, 3), font=('Courier', 13, "bold"))],
                      [text_temp("1")],
                      [text_temp("2")],
                      [text_temp("3")],
                      [text_temp("4")],
                      [text_temp("5")]]

    name_column = [[sg.Text("\nName",justification="center", size=(10, 3), font=('Courier', 13, "bold"))],
                   [text_temp(scores[0]["name"])],
                   [text_temp(scores[1]["name"])],
                   [text_temp(scores[2]["name"])],
                   [text_temp(scores[3]["name"])],
                   [text_temp(scores[4]["name"])]]

    score_column = [[sg.Text("\nScore",justification="center", size=(10, 3), font=('Courier', 13, "bold"))],
                    [text_temp(locale.currency(scores[0]["score"], grouping=True))],
                    [text_temp(locale.currency(scores[1]["score"], grouping=True))],
                    [text_temp(locale.currency(scores[2]["score"], grouping=True))],
                    [text_temp(locale.currency(scores[3]["score"], grouping=True))],
                    [text_temp(locale.currency(scores[4]["score"], grouping=True))]]



    layout = [[sg.Text("DopeWars", justification='center', size=(100, 1), font=('Courier', 50, "underline"))],
              [sg.Text(size=(100, 1)),],
              [sg.Text(size=(40, 1)),
               sg.Button("Play Again", auto_size_button=True, key="play")],
              [sg.Text("", size=(21, 300)),
               sg.Column(numbers_column, size=(120, 300)),
               sg.Column(name_column, size=(130, 300)),
               sg.Column(score_column, size=(130, 300))],
              ]



    window = sg.Window("DopeWars", layout, size=(800, 600))

    while True:
        event, values = window.read()

        if event ==  sg.WINDOW_CLOSED:
            break

        if event == "play":
            name_entry_win()
            break

    window.close()


def main():
    name_entry_win()

if __name__ == "__main__":
    main()






