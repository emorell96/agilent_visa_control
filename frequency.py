class FreqUnit:
    Hz, kHz, MHz, GHz = [(i, 1000**i) for i in range(4)]
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
    __rmul__ = __mul__
    def __init__(self, value, unit: FreqUnit, time = None):
        self.time = time
        self.value = value
        self.unit = unit
    def __str__(self):
        return "{0:.1f} {1}".format(self.value, self.unit)
    def convert(self, targetunit: FreqUnit):
        coeff1 = self.unit[1]
        coeff2 = targetunit.value[1]
        if coeff1 != coeff2:
            return Frequency(self.value*coeff1/coeff2, targetunit, self.time)        
    def __mul__(self, other, unit_size = None):
        if self.unit == other.unit:
            return Frequency(self.value*other.value, self.unit, self.time)
        return self.convert(FreqUnit(FreqUnit.Hz))*self.convert(FreqUnit(FreqUnit.Hz))
        