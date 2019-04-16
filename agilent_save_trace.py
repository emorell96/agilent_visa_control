import configparser
import math as m
import AgilentClass  as ag
from frequency import *
import numpy as np

""" visa.logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
visa.logger.addHandler(ch) """

#outline of the code:
# 1. create a visa resource manager
# 2. initializes communication with the agilent sa
# 3. set marker at modulation frequency
# 4. read periodically (t) the power of such peak from the marker using

#rm.list_resources()

#global variables:
#-----------------------------------

#variables:

identifier = "GPIB0::8::INSTR"
#traces to be read:
traces = (1,)

print("Reading {0} traces from the VISA resource: {}".format(len(traces), identifier))

#Reading configuration file to avoid overwriting any data
out_path = r"Z:\Lasers\L850P200\Agilent Code\data_{0}.txt"
config_file = r"Z:\Lasers\L850P200\Agilent Code\config.txt"

configParser = configparser.RawConfigParser()   
configParser.read(config_file)

#changes the name of the output file
next_out = int(configParser.get('Output Settings', 'next_out'))
out_path = out_path.format(next_out)
#number of points in digital conversion
points = 1024

#set up of the agilent using the class:
#this is the object representing the spectrum analyzer.
agilent = ag.Agilent(identifier)
#open
agilent.open()
agilent.set_sa()

#setting the center frequency and the span of the spectrum analyzer
modulation_freq = Frequency(80.1, FreqUnit(FreqUnit.MHz))
span = Frequency(50, FreqUnit(FreqUnit.kHz))

#setting the y axis options
ref_level = 3 #in dBm
scale = 10 #in dBm per Div

#sends instructions to the agilent
agilent.set_marker(1, modulation_freq)
agilent.set_x(modulation_freq, span)

agilent.set_y(ref_level, scale) #in dBm
agilent.set_points(points)

freq_values = [span.value/points*i+modulation_freq.value-(span.value/2.0) for i in range(points)]
values = agilent.get_trace(1)
#close agilent connection
agilent.close()

#save into a file
np.savetxt(out_path, (freq_values, values))
