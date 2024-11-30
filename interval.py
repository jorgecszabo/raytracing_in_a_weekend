import numpy as np

class Interval:
    def __init__(self, min, max):
        self.min, self.max = min, max

    def contains(self, x):
        return self.min <= x <= self.max

    def surrounds(self, x):
        return self.min < x < self.max

    @classmethod
    def empty(cls):
        return cls(+np.inf, -np.inf)

    @classmethod
    def universe(cls):
        return cls(-np.inf, +np.inf)