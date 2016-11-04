import abc


class DecayFunction(metaclass=abc.ABCMeta):
    """
    Base class for decay functions, implemented with a strategy design pattern
    """
    def __init__(self, init_value):
        self._value = init_value

    @property
    def value(self):
        return self._value

    @abc.abstractmethod
    def decay(self):
        pass


class StaticDecay(DecayFunction):
    """
    Not really a decay function. But since asked for, implemented as one.
    """
    def decay(self):
        pass


class LinearDecay(DecayFunction):
    """
    Decaying with a constant rate
    """
    def __init__(self, start_value, rate):
        self.rate = rate
        super().__init__(start_value)

    def decay(self):
        self._value -= self.rate


class ExponentialDecay(DecayFunction):
    """
    Decaying exponential.
    """
    def __init__(self, start_value, rate):
        self.rate = rate
        super().__init__(start_value)

    def decay(self):
        self._value *= self.rate
