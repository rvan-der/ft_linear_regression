import sys
import json
from parsing_tools import *
from predictor import estimate_price



class WeightsSavingError(Exception):
    def __init__(self,message=""):
        # Exception.__init__(message)
        self.message = message



def train_model(nbIterations, theta0, theta1, data):
    learning_rate = 0.000000001
    data_size = len(data)

    for _ in range(nbIterations):
        gradient_t0, gradient_t1 = 0, 0
        for car in data:
            estimation = estimate_price(car["km"], theta0, theta1)
            gradient_t0 += estimation - car["price"]
            gradient_t1 += (estimation - car["price"]) * car["km"]
        print(gradient_t0, gradient_t1)
        gradient_t0 /= data_size
        gradient_t1 /= data_size
        theta0 -= learning_rate * gradient_t0
        theta1 -= learning_rate * gradient_t1

    return {"theta0": theta0, "theta1": theta1}



def save_weights(theta0, theta1):
    fd = None
    try:
        fd = open("weights.json", mode="w")
    except FileNotFoundError:
        print_warning_msg("Warning:\nWeights file not found. Saving updated weights to new file 'weights.json'.")
        fd = None
    except:
        print_error_msg("An error occured while trying to open the weights file. Saving failed.", _exit=True)
    if fd == None:
        try:
            fd = open("weights.json", mode="x")
        except:
            print_error_msg("An error occured while trying to save the weights to new file. Saving failed.", _exit=True)
    if fd != None:
        try:
            json.dump({"theta0": theta0, "theta1": theta1}, fd)
        except:
            print_error_msg("An error occured while trying to write to the weigths file. Saving failed.", _exit=True)




if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 2:
        print_error_msg("Missing number of iterations as argument.", _exit=True)
    if argc > 2:
        print_error_msg("Too many arguments.", _exit=True)
    try:
        nbIterations = int(sys.argv[1])
    except:
        print_error_msg("Number of iterations must be an integer >= 1.", _exit=True)
    if nbIterations < 1:
        print_error_msg("Number of iterations must be an integer >= 1.", _exit=True)

    try:
        data = read_csv("data.csv")
    except DataLoadingError as err:
        print_error_msg("Couldn't load the data:\n" + err.message, _exit=True)
    except:
        print_error_msg("Couldn't load the data.", _exit=True)

    # print(*[(car["km"],car["price"]) for car in data], sep='\n')

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

    weights = train_model(nbIterations, theta0, theta1, data)

    save_weights(weights["theta0"], weights["theta1"])
    print(f"new weights: %f, %f"%(weights["theta0"], weights["theta1"]))
    