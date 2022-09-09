import sys
import json

from PySide6.QtCore import QRunnable, Slot, Signal
from parsing_tools import *
from visualizator.visualizator import launch_visualizator


class Trainer(QRunnable):

    weights_updated = Signal(dict)

    def __init__(self, weights, data, nbIterations, qt=True):
        QRunnable.__init__()

    @Slot()
    def run(self):
        self.train_model(self.weights, self.data, self.nbIterations)


    def train_model(weights, data, nbIterations, qt=False):
        learning_rate = 0.01
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
            weights["theta0"] -= learning_rate * gradient_t0
            weights["theta1"] -= learning_rate * gradient_t1
            if qt and not i % (nbIterations // nbAnimationPoints) and i != nbIterations - 1 :
                self.weights_updated.emit(weights)

        if qt:
            self.weights_updated.emit(weights)
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
    argc = len(sys.argv)
    if argc > 2:
        print_error_msg("Too many arguments.", _exit=True)
    if argc == 2:
        if sys.argv[1] != "-v":
            print_error_msg("This option doesn't exist.", _exit=True)
        else:
            launch_visualizator()
    else:
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

        data, norm_factor = Trainer.normalize_data(data, weights["norm_factor"])

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
                weights = Trainer.train_model(weights, data, nbIterations)
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
    