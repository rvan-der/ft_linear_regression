import sys
from parsing_tools import *


def estimate_price(distance, theta0=0, theta1=0):
    return theta1 * distance + theta0


if __name__ == "__main__":

    argc = len(sys.argv)
    if argc < 2:
        print_error_msg("Missing distance argument.")
        exit()
    if argc > 2:
        print_error_msg("Too many arguments.")
        exit()

    distance = 0
    try:
        distance = int(sys.argv[1])
    except:
        print_error_msg("Distance must be a positive integer.")
        exit()
    if distance < 0:
        print_error_msg("Distance must be a positive integer.")
        exit()

    theta0 = 0
    theta1 = 0
    try:
        weights = load_weights()
    except WeightsLoadingError as err:
        print_warning_msg("Warning:\n" + err.message + " Weights are set to 0.")
    except:
        print_warning_msg("Warning:\nCouldn't load the weights. Weights are set to 0.")
    else:
        theta0 = weights["theta0"]
        theta1 = weights["theta1"]
   

    print("Estimated price:", estimate_price(distance, theta0, theta1))
