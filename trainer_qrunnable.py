from PySide6.QtCore import QRunnable, QObject, Slot, Signal
import time


class TrainerSignals(QObject):

    weights_updated = Signal(dict)
    job_finished = Signal(dict)



class Trainer(QRunnable):

    def __init__(self, weights, data, nbIterations, learningRate=0.1):
        super(Trainer, self).__init__()
        self.weights = weights
        self.data = data
        self.nbIterations = nbIterations
        self.learningRate = learningRate
        self.signals = TrainerSignals()


    @Slot()
    def run(self):
        self.train_model(self.weights, self.data, self.nbIterations, learningRate=self.learningRate)


    def train_model(self, weights, data, nbIterations, learningRate=0.1):
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
            if not i % (nbIterations // nbAnimationPoints) and i != nbIterations - 1 :
                time.sleep(0.015)
                self.signals.weights_updated.emit(weights)

        self.signals.job_finished.emit(weights)
        return weights