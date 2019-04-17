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
        if self.value == FreqUnit.Hz:
            return "Hz"
    def __eq__(self, y):
        return self.value == y.value
    def __pow__(self, x):
        if x == 2:
            id = self.value[0]
            return SqFreqUnit((id, 1000**(2*id)))
class SqFreqUnit:
    sqHz, sqkHz, sqMHz, sqGHz = [(i, 1000**(2*i)) for i in range(4)]
    def __init__(self, Type):
        self.value = Type
    def __str__(self):
        if self.value == SqFreqUnit.sqMHz:
            return u"MHz²"
        if self.value == SqFreqUnit.sqGHz:
            return u"GHz²"
        if self.value == SqFreqUnit.sqkHz:
            return u"kHz²"
        if self.value == SqFreqUnit.sqHz:
            return u"Hz²"
    def __eq__(self, y):
        return self.value == y.value    
class Frequency:
    
    def __init__(self, value, unit: FreqUnit, time = None):
        self.time = time
        self.value = value
        self.unit = unit
    def __str__(self):
        return "{0:.3f} {1}".format(self.value, self.unit)
    def convert(self, targetunit: FreqUnit):
        coeff1 = self.unit.value[1]
        coeff2 = targetunit.value[1]
        if coeff1 != coeff2:
            return Frequency(self.value*coeff1/coeff2, targetunit, self.time)
        else:
            return self        
    def __mul__(self, other, targetunit = FreqUnit(FreqUnit.Hz)):
        #multiplication of freq * freq so final unit is sqfreq
        if self.unit == other.unit:
            return Frequency(self.value*other.value, self.unit**2, self.time)
        return self.convert(targetunit)*other.convert(targetunit)
    def __rmul__(self, const):
        #multiplication by a constant ( unit is kept the same):
        return Frequency(const * self.value, self.unit, self.time)
         
    def __add__(self, other, targetunit = FreqUnit(FreqUnit.Hz)):
        if self.unit == other.unit:
            return Frequency(self.value+other.value, self.unit, self.time)
        return self.convert(targetunit)+other.convert(targetunit)
    __radd__ = __add__


if __name__ == "__main__":
    #usage:
    freq1 = Frequency(50, FreqUnit(FreqUnit.MHz))
    freq2 = Frequency(1, FreqUnit(FreqUnit.GHz))
    print((freq1*freq2).convert(SqFreqUnit(SqFreqUnit.sqMHz)))
    print(2*freq1)
    print((freq1+freq2).convert(FreqUnit(FreqUnit.Hz)))
    print(freq1.__mul__(freq2, FreqUnit(FreqUnit.MHz)))