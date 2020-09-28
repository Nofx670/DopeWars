import PySimpleGUI as sg
import random
import csv
import locale
from dopewars import functions as dw

locale.setlocale(locale.LC_ALL, "")

weed = dw.Drugs("Weed", 36, 60, 5, quantity=random.randint(1, 150))
coke = dw.Drugs("Coke", 3745, 30000, 2500, quantity=random.randint(1, 150))
heroin = dw.Drugs("Heroin", 1892, 9000, 1000, quantity=random.randint(1, 150))
acid = dw.Drugs("Acid", 67, 80, 10, quantity=random.randint(1, 150))
meth = dw.Drugs("Meth", 376, 1000, 70, quantity=random.randint(1, 150))
hash = dw.Drugs("Hash", 12, 40, 5, quantity=random.randint(1, 150))

player = dw.Player("", 1000, 100)

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

                if dw.make_buy_deal(int(values["quantity"]), values["product"], drugs, player) == True:
                    #updates the product shown in the players inventory
                    window[values["product"]].update(str(player.inventory[values["product"]]))
                    #updates the amount of product shown available to buy
                    window[values["product"]+"_"].update(drugs[values["product"]].quantity)
                    #updates the players available cash shown
                    window["player cash"].update("\n"+locale.currency(player.money, grouping=True))
                    #updates the price paid column shown
                    window[values["product"]+"p"].update(locale.currency(dw.average_price_paid(drugs[values["product"]].value,
                                                                       price2,
                                                                       int(values["quantity"]),
                                                                       quan2,
                                                                       values["product"],
                                                                       drugs), grouping=True))

            except:

                pass

        if event == "Sell":
            try:
                dw.make_sell_deal(int(values["quantity"]), values["product"], drugs, player)
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
            dw.set_new_month(drugs, player)
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



name_entry_win()






