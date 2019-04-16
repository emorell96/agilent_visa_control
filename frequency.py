class FreqUnit:
    MHz, GHz, kHz = range(1,4)
    def __init__(self, Type):
        self.value = Type
    def __str__(self):
        if self.value == FreqUnit.MHz:
            return "MHz"
        if self.value == FreqUnit.GHz:
            return "GHz"
        if self.value == FreqUnit.kHz:
            return "kHz"
    def __eq__(self, y):
        return self.value == y.value
class Frequency:
    def __init__(self, value, unit: FreqUnit, time = None):
        self.time = time
        self.value = value
        self.unit = unit
    def __str__(self):
        return "{0:.1f} {1}".format(self.value, self.unit)