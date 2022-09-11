from PySide6.QtCore import QRunnable, Slot, Signal


class Trainer(QRunnable):

    weights_updated = Signal(dict)
    job_finished = Signal(dict)

    def __init__(self, weights, data, nbIterations):
        super(QRunnable).__init__()
        self.weights = weights
        self.data = data
        self.nbIterations = nbIterations

    @Slot()
    def run(self):
        self.train_model(self.weights, self.data, self.nbIterations, qt=True)


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
            self.job_finished.emit(weights)
        return weights