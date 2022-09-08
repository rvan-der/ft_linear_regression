import sys
import random
from parsing_tools import *


def estimate_price(distance, theta0=0, theta1=0, norm_factor=1):
    distance /= norm_factor
    estimation = theta1 * distance + theta0
    return round(estimation * norm_factor)


if __name__ == "__main__":
    currencies = ["$ ", "¥ ", "₡ ", "₱ ", "£ ", "€ ", "¢ ", "₩ ", "₭ ", "₮ ", "₦ ", " gold coins", "₽ ", "฿ ", "₺ ", "₴ ", " nickels", " credits", " darseks", " flanian pobble beads", " kalganids", " silver coins", " copper coins", " simoleons", " robux", " emeralds", " silver eagles", " ningis", "triganic pus"]

    theta0 = 0
    theta1 = 0
    norm_factor = 1
    try:
        weights = load_weights()
    except WeightsLoadingError as err:
        print_warning_msg("Warning:\n" + err.message + " Weights are set to 0.")
    except:
        print_warning_msg("Warning:\nCouldn't load the weights. Weights are set to 0.")
    else:
        theta0 = weights["theta0"]
        theta1 = weights["theta1"]
        norm_factor = weights["norm_factor"]

    print("Welcome to rvan-der's car price predictor for ft_linear_regression !")

    while True:
        check = False
        while not check:
            check = True
            distance = input("\nTell me how many km the car has traveled and i'll tell you its price.\n> ")
            try:
                distance = float(distance)
            except:
                print("The distance must be a positive number. Try again !")
                check = False
            else:
                if distance < 0:
                    print("The distance must be a positive number. Try again !")
                    check = False
        print("Your car is worth %d%s."%(estimate_price(distance, theta0, theta1, norm_factor), random.choice(currencies)))
        print("\nDo you want to know the price of another car ? (y/n)")
        yn=""
        while yn.lower().strip() not in ["yes", "sure", "yeah", "yea", "yep", "yup", "oui", "y3s", "y", "no", "n", "n0", "nope", "non"]:
            yn = input("> ")
        if yn.lower().strip() in ["no", "n", "n0", "nope", "non"]:
            print("\nOk bye !")
            exit()
