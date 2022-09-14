import sys
import json

from io_tools import *
from visualizer.visualizer import launch_visualizer


def train_model(weights, data, nbIterations, learningRate=0.1):
    dataSize = len(data)
    nbAnimationPoints = min(nbIterations, 100)

    for i in range(nbIterations):
        gradient_t0, gradient_t1 = 0, 0
        for car in data:
            estimation = weights["theta1"] * car["km"] + weights["theta0"]
            gradient_t0 += estimation - car["price"]
            gradient_t1 += (estimation - car["price"]) * car["km"]
        gradient_t0 /= dataSize
        gradient_t1 /= dataSize
        weights["theta0"] -= learningRate * gradient_t0
        weights["theta1"] -= learningRate * gradient_t1

    return weights


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
    argc = len(sys.argv)
    if argc > 2:
        print_error_msg("Too many arguments.", _exit=True)

    if argc == 2:
        if sys.argv[1] != "-v":
            print_error_msg("This option doesn't exist.", _exit=True)
        else:
            launch_visualizer()

    else:
        try:
            data = read_csv("data.csv")
        except Exception as e:
            print_error_msg("Couldn't load the data:\n" + str(e) + "\nexiting...", _exit=True)

        try:
            weights = load_weights()
        except Exception as e:
            print_warning_msg("Warning:\n" + str(e) + " Weights are set to 0.")
            weights = {"theta0": 0, "theta1": 0, "norm_factor": 0}

        normalizedData = normalize_data(data, weights)

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
                weights = train_model(weights, normalizedData, nbIterations)
                try:
                    save_weights(weights)
                except WeightsSavingError as e:
                    print_error_msg(e.message)
                print("finished !\nNew weights (for data normalized with a factor of 1/%d): T0 = %f ; T1 = %f"%(weights["norm_factor"], weights["theta0"], weights["theta1"]))
            
            print("\nDo you want to continue training ? (y/n)")
            yn=""
            while yn.lower().strip() not in ["ye", "yes", "sure", "yeah", "yea", "yep", "yup", "oui", "y3s", "y", "no", "n", "n0", "nope", "non"]:
                yn = input("> ")
            if yn.lower().strip() in ["no", "n", "n0", "nope", "non"]:
                print("\nOk bye !")
                exit()
    