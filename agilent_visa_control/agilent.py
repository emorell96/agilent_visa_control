import visa
from agilent_visa_control.frequency import Frequency, FreqUnit, SqFreqUnit

class Agilent:
    #commands:

    #command for setting the mode as the Spectrum Analyser
    sa = "INST:NSEL 1"
    #command for setting ref level:
    ref_level_command = ":DISP:WIND:TRACE:Y:RLEVEL {0:.2f} dBm"
    #command for setting the scale per div
    scale_command = ":DISP:WIND:TRACE:Y:PDIV {0:.2f} dB"

    #command for span with format
    span_command = "FREQ:SPAN {0:.2f} {1}"
    #command for setting the center freq
    center_command = "FREQ:CENTER {0:.2f} {1}"
    #set marker mode normal
    marker_on = ":CALC:MARK{0}:MODE POS"
    #set marker at modulation freq
    marker_command = ":CALC:MARK{0}:X {1:.2f} {2}"
    #ask marker value
    marker_query = ":CALC:MARK{0}:Y?"
    #format trace in ascii:
    form_ascii = ":FORM ASCii"
    #get trace
    trace_query = ":TRACe:DATA?  TRACE{0}"
    #points set up command
    points_command = ":SWE:POIN {0}"
    points_query = ":SWE:POIN?"
    def __init__(self, identifier, marker_number = 1):
        self.identifier = identifier
        self.markers = [ False for i in range(1,13)]
        self.marker_number = marker_number
        self.rm = visa.ResourceManager()
    def open(self):
        self.ag =  self.rm.open_resource(self.identifier)
    def set_sa(self):
        self.ag.write(self.sa)
    def set_format(self, format = "ascii"):
        if format == "ascii":
            self.ag.write(self.form_ascii)
        else:
            #code other formats (real, int32 etc)
            pass
    def set_x(self, center: Frequency, span: Frequency):
        self.center = center
        self.span = span
        self.ag.write(self.span_command.format(span.value, span.unit))
        self.ag.write(self.center_command.format(center.value, center.unit))
    def set_y(self, ref_level, scale):
        #in dBm
        self.ref_level = ref_level
        self.scale = scale
    def setMarkerOn(self, marker: int):
        """
        Sets the internal array of markers to on.
        ATTENTION: IT DOESN'T INTERACT WITH THE INSTRUMENT, USE WITH CAUTION
        """
        self.markers[marker-1] = True
    def set_points(self, points):
        try:
            self.points = int(points)
        except ValueError:
            print("points is not an integer!!!")
            print("Setting 256 points as default")
            self.points = 256
        self.ag.write(self.points_command.format(self.points))
    def get_points(self):
        self.points = self.ag.query_ascii_values(self.points_query)
        return self.points
    def __turnmarker_on(self, marker: int):
        self.ag.write(self.marker_on.format(marker))
        self.markers[marker-1] = True
    def __marker_on(self, marker: int):
        return self.markers[marker-1]
    def set_marker(self, marker: int, marker_freq : Frequency):
        if not self.__marker_on(marker):
            self.__turnmarker_on(marker)
        self.ag.write(self.marker_command.format(marker, marker_freq.value, marker_freq.unit))
    def get_marker(self, marker: int):
        if not self.__marker_on(marker):
            print("Error! Trying to query an unset marker!")
            exit()
        return self.ag.query_ascii_values(self.marker_query.format(marker))[0]
    def get_trace(self, trace):
        #check that trace is either 1, 2 or 3
        if trace in (1,2,3):
            return self.ag.query_ascii_values(self.trace_query.format(trace))

    def close(self):
        self.ag.close()

# #Usage:
if __name__ == "__main__":
    identifier = "GPIB0::8::INSTR"
    agilent = Agilent(identifier)

    agilent.open()

    agilent.set_sa()
    modulation_freq = Frequency(80.1, FreqUnit(FreqUnit.MHz))
    span = Frequency(50, FreqUnit(FreqUnit.kHz))

    agilent.set_marker(1, modulation_freq)
    agilent.set_x(modulation_freq, span)

    agilent.set_y(3, 10) #in dBm
    values = agilent.get_trace(1)
    print(values)
    print(agilent.get_marker(1))

    agilent.close()
