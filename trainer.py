import sys
import json
from parsing_tools import *
from visualizator.visualizator import launch_visualizator



def train_model(weights, data, nbIterations, learning_rate=0.01):
    data_size = len(data)
    theta0=weights["theta0"]
    theta1=weights["theta1"]

    for _ in range(nbIterations):
        gradient_t0, gradient_t1 = 0, 0
        for car in data:
            estimation = theta1 * car["km"] + theta0
            gradient_t0 += estimation - car["price"]
            gradient_t1 += (estimation - car["price"]) * car["km"]
        gradient_t0 /= data_size
        gradient_t1 /= data_size
        theta0 -= learning_rate * gradient_t0
        theta1 -= learning_rate * gradient_t1

    weights["theta0"] = theta0
    weights["theta1"] = theta1
    return weights



def normalize_data(data, norm_factor=0):
    if not norm_factor:
        max_km = max(data, key=lambda e: e["km"])["km"]
        max_price = max(data, key=lambda e: e["price"])["price"]
        norm_factor = max(max_km, max_price)

    new_data = []
    for car in data:
        new_car = {"km": car["km"] / norm_factor, "price": car["price"] / norm_factor}
        new_data.append(new_car)
    return (new_data, norm_factor)



def verify_trainer_answer(answer):
    try:
        answer = int(answer)
    except:
        print("Training can only be performed a positive whole number of times. Try again !")
        return False
    if answer < 0:
        print("Training can only be performed a positive whole number of times. Try again !")
        return False
    return True



if __name__ == "__main__":
    try:
        data = read_csv("data.csv")
    except DataLoadingError as err:
        print_error_msg("Couldn't load the data:\n" + err.message + "\nexiting...", _exit=True)
    except:
        print_error_msg("Couldn't load the data.\nexiting...", _exit=True)

    try:
        weights = load_weights()
    except WeightsLoadingError as err:
        print_warning_msg("Warning:\n" + err.message + " Weights are set to 0.")
        weights = {"theta0": 0, "theta1": 0, "norm_factor": 0}
    except:
        print_warning_msg("Warning:\nCouldn't load the weights. Weights are set to 0.")
        weights = {"theta0": 0, "theta1": 0, "norm_factor": 0}

    data, norm_factor = normalize_data(data, weights["norm_factor"])

    print("\nWelcome to rvan-der's model training program for ft_linear_regression !\n\
Launch with option -v for visualization and bonuses.")

    while True:

        check = False
        while not check:
            nbIterations = input("\nHow many iterations of training would you like to perform ?\n> ")
            check = verify_trainer_answer(nbIterations)

        nbIterations = int(nbIterations)
        if nbIterations == 0:
            print("Nothing was performed.")
        else:
            print("training model... ", end="", flush=True)
            weights = train_model(weights, data, nbIterations)
            try:
                save_weights(weights["theta0"], weights["theta1"], norm_factor)
            except WeightsSavingError as e:
                print_error_msg(e.message)
            print("finished !\nNew weights (for data normalized with a factor of 1/%d): T0 = %f ; T1 = %f"%(norm_factor, weights["theta0"], weights["theta1"]))
        
        print("\nDo you want to continue training ? (y/n)")
        yn=""
        while yn.lower().strip() not in ["yes", "sure", "yeah", "yea", "yep", "yup", "oui", "y3s", "y", "no", "n", "n0", "nope", "non"]:
            yn = input("> ")
        if yn.lower().strip() in ["no", "n", "n0", "nope", "non"]:
            print("\nOk bye !")
            exit()
    