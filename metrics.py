import numpy as np

class Loss:
    def __init__(self, loss=None, derivative=None, dp=0.1, centering=0):
        if loss is not None:
            self.loss = loss
            if derivative is not None:
                self.derivative = derivative
            else:
                # Symmetric derivative
                if centering == 0:
                    self.derivative = lambda p, y : (loss(p+0.5*dp, y) - loss(p-0.5*dp, y)) / dp
                # Right derivative
                elif centering == 1:
                    self.derivative = lambda p, y : (loss(p+dp, y) - loss(p, y)) / dp
                # Left derivative
                elif centering == -1:
                    self.derivative = lambda p, y : (loss(p, y) - loss(p-dp, y)) / dp
                else:
                    raise ValueError("Centering value is invalid. Must be integer of 0, 1 or -1.")
        else:
            self.loss = lambda p, y : (1/2) * ((p-y).transpose() @ (p-y)).diagonal()
            self.derivative = lambda p, y : p - y

    def evaluate(self, pred, y):
        return self.loss(np.asmatrix(pred), np.asmatrix(y))

    def gradient(self, pred, y):
        return self.derivative(np.asmatrix(pred), np.asmatrix(y))


class MeanSquaredError(Loss):
    def __init__(self):
        loss = lambda p, y : (1/(2*y.shape[0])) * ((p-y).transpose() @ (p-y)).diagonal()
        derivative = lambda p, y : (1/(y.shape[0])) * (p-y).sum(0)
        super().__init__(loss=loss, derivative=derivative)


class MeanAbsoluteError(Loss):
    def __init__(self):
        loss = lambda p, y : (1/(y.shape[0])) * np.abs(p-y).sum(0)
        derivative = lambda p, y : (1/(y.shape[0])) * np.multiply(p-y, 1/np.abs(p-y)).sum(0)
        super().__init__(loss=loss, derivative=derivative)
