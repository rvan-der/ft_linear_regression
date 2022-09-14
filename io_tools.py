import sys
import json
import os



class WeightsSavingError(Exception):
    def __init__(self,message=""):
        super(WeightsSavingError, self).__init__()
        self.message = message

    def __str__(self):
        return self.message



class DataLoadingError(Exception):
    def __init__(self, message=""):
        super(DataLoadingError, self).__init__()
        self.message = message

    def __str__(self):
        return self.message



class WeightsLoadingError(Exception):
    def __init__(self, message=""):
        super(WeightsLoadingError, self).__init__()
        self.message = message

    def __str__(self):
        return self.message



class WeightsDeletionError(Exception):
    def __init__(self, message=""):
        super(WeightsDeletionError, self).__init__()
        self.message = message

    def __str__(self):
        return self.message



def print_error_msg(msg, _exit=False):
    print("\033[91m" + msg + "\033[0m", file=sys.stderr, flush=True)
    if _exit:
        exit()



def print_warning_msg(msg):
    print("\033[93m" + msg + "\033[0m", file=sys.stderr, flush=True)



def delete_weights_file():
    try:
        os.remove("weights.json")
    except Exception as e:
        raise WeightsDeletionError("Failed to delete the weights file: " + str(e))



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
    except Exception as e:
        raise WeightsLoadingError("Couldn't open the weights file: %s."%(str(e)))
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
            if not all([x in weights for x in ["theta0", "theta1", "norm_factor"]]):
                fd.close()
                raise WeightsLoadingError("Missing data in the weights file.")
            if not all([isinstance(weights[x], (float, int)) for x in ["theta0", "theta1", "norm_factor"]]):
                fd.close()
                raise WeightsLoadingError("Invalid data in the weights file.")
        fd.close()
    return weights



def save_weights(weights):
    fd = None
    try:
        fd = open("weights.json", mode="w")
    except FileNotFoundError:
        try:
            fd = open("weights.json", mode="x")
        except:
            raise WeightsSavingError("An error occured while trying to save the weights to new a file. Saving failed.")
    except:
        raise WeightsSavingError("An error occured while trying to open the weights file. Saving failed.")
    try:
        json.dump(weights, fd)
    except:
        raise WeightsSavingError("An error occured while trying to write to the weigths file. Saving failed.")



def normalize_data(data, weights):
    if not weights["norm_factor"]:
        max_km = max(data, key=lambda e: e["km"])["km"]
        max_price = max(data, key=lambda e: e["price"])["price"]
        weights["norm_factor"] = max(max(max_km, max_price), 1)

    new_data = []
    for car in data:
        new_car = {"km": car["km"] / weights["norm_factor"], "price": car["price"] / weights["norm_factor"]}
        new_data.append(new_car)
    return new_data



def condensed_notation(n, maxChars):
    strn = str(n)
    if len(strn) <= maxChars:
        return strn

    strn = "%f"%(n)
    intRange = strn.find(".")
    if intRange == maxChars or intRange == maxChars - 1:
        return str(round(n))

    if intRange < maxChars:
        s = "{:.%df}"%(maxChars - 1 - intRange)
        return s.format(n)
        
    power = str(intRange - 1 - int(n < 0))
    sigFigs = max(0, maxChars - len(power) - int(n < 0) - 3)
    s = "{:.%de}"%(sigFigs)
    s = s.format(n).split("+")
    return s[0] + power
