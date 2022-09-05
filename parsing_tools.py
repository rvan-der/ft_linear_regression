import sys
import json



class DataLoadingError(Exception):
    def __init__(self, message=""):
        # Exception.__init__()
        self.message = message



class WeightsLoadingError(Exception):
    def __init__(self, message=""):
        # Exception.__init__()
        self.message = message



def print_error_msg(msg, _exit=False):
    print("\033[91m" + msg + "\033[0m", file=sys.stderr, flush=True)
    if _exit:
        exit()



def print_warning_msg(msg):
    print("\033[93m" + msg + "\033[0m", file=sys.stderr, flush=True)



def read_csv(fileName):
    try:
        fd = open(fileName)
    except Exception as e:
        raise DataLoadingError(str(e))
    keys,*lines = fd.read().split('\n')
    fd.close()

    keys = keys.split(',')
    nbKeys = len(keys)
    if nbKeys != 2:
        raise DataLoadingError("Incorrect number of columns.")
    if set(keys) != {"km","price"}:
        raise DataLoadingError("Wrong column names: " + ", ".join(keys))

    data = []
    for line in lines:
        if line == '':
            continue
        values = line.split(',')
        if len(values) != nbKeys:
            raise DataLoadingError("The format of the csv file is wrong.")
        item = {}
        for key,value in zip(keys, values):
            try:
                value = float(value)
                item[key] = value
            except ValueError:
                raise DataLoadingError("Data must contain only numerical values.")
            if key == 'km' and value < 0:
                raise DataLoadingError("Data can't contain negative values for distance.")
        data.append(item)
    return data



def load_weights(fileName="weights.json"):
    weights = None
    try:
        fd = open(fileName)
    except FileNotFoundError:
        raise WeightsLoadingError("Didn't find the weights file.")
    except:
        raise WeightsLoadingError("Couldn't open the weights file.")
    if fd:
        try:
            weights = json.load(fd)
        except Exception as e:
            fd.close()
            raise WeightsLoadingError("Couldn't load json object from the weights file: " + str(e))
        else:
            if not isinstance(weights, dict):
                fd.close()
                raise WeightsLoadingError("Invalid data in the weights file.")
            if "theta0" not in weights or "theta1" not in weights:
                fd.close()
                raise WeightsLoadingError("Missing data in the weights file.")
            if not isinstance(weights["theta0"], (float, int)) or not isinstance(weights["theta1"], (float, int)):
                fd.close()
                raise WeightsLoadingError("Invalid data in the weights file.")
        fd.close()
    return weights



def normalize_data(data):
    min_km = min(data, key=lambda e: e["km"])["km"]
    max_km = max(data, key=lambda e: e["km"])["km"]
    min_price = min(data, key=lambda e: e["price"])["price"]
    max_price = max(data, key=lambda e: e["price"])["price"]
    new_data = []
    for car in data:
        new_car = {"km": (car["km"] - min_km) / max_km, "price": (car["price"] - min_price) / max_price}
        new_data.append(new_car)
    return new_data
