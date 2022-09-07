import sys
import json
from parsing_tools import *
from visualizator.visualizator import launch_visualizator



def train_model(nbIterations, theta0, theta1, data, learning_rate=0.01):
    data_size = len(data)

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
    print(f"gradients: {gradient_t0} , {gradient_t0}")
    return {"theta0": theta0, "theta1": theta1}



def normalize_data(data, norm_factor=None):
    if not norm_factor:
        max_km = max(data, key=lambda e: e["km"])["km"]
        max_price = max(data, key=lambda e: e["price"])["price"]
        norm_factor = max(max_km, max_price)

    new_data = []
    for car in data:
        new_car = {"km": car["km"] / norm_factor, "price": car["price"] / norm_factor}
        new_data.append(new_car)
    return (new_data, norm_factor)




if __name__ == "__main__":
    try:
        data = read_csv("data.csv")
    except DataLoadingError as err:
        print_error_msg("Couldn't load the data:\n" + err.message + "\nexiting...", _exit=True)
    except:
        print_error_msg("Couldn't load the data.\nexiting...", _exit=True)

    theta0 = 0
    theta1 = 0
    norm_factor=None
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

    data, norm_factor = normalize_data(data, norm_factor)

    weights = train_model(nbIterations, theta0, theta1, data)

    try:
        save_weights(weights["theta0"], weights["theta1"], norm_factor)
    except WeightsSavingError as e:
        print_error_msg(e.message)
    except WeightsSavingWarning as w:
        print_warning_msg(e.message)

    print(f"new weights: %f, %f"%(weights["theta0"], weights["theta1"]))
    