import abc

class DecayFunction(metaclass=abc.ABCMeta):
    def __init__(self, init_value):
        self._value = init_value

    @property
    def value(self):
        return self._value

    @abc.abstractmethod
    def decay(self):
        pass

class StaticDecay(DecayFunction):
    def decay(self):
        pass

class LinearDecay(DecayFunction):
    def __init__(self, start_value, rate):
        self.rate = rate
        super().__init__(start_value)

    def decay(self):
        self._value -= self.rate


class ExponentialDecay(DecayFunction):
    def __init__(self, start_value, rate):
        self.rate = rate
        super().__init__(start_value)

    def decay(self):
        self._value *= self.rate
