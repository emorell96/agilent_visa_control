import visa
import logging
import time
from datetime import datetime
import serial
import configparser
import math as m
from temperature import *
from tektronix2000 import *
from threading import Event, Thread, Timer

""" visa.logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
visa.logger.addHandler(ch) """
rm = visa.ResourceManager()

class RepeatedTimer:

    """Repeat `function` every `interval` seconds."""

    def __init__(self, interval, max_runs, function, closefunc, *args, **kwargs):
        #set max_runs = -1 to inf
        self.max_runs = max_runs
        self.interval = interval
        self.closefunc = closefunc
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.runs = 0
        self.start = time.time()
        self.event = Event()
        self.thread = Thread(target=self._target)
        self.thread.start()


    def _target(self):
        while not self.event.wait(self._time):
            self.function(*self.args, **self.kwargs)
            self.runs += 1
            if(not self.runs % 100):
                print("Function {2} has run {0} times, {1} times to go.".format(self.runs, self.max_runs - self.runs if self.max_runs > 0 else "infinity", self.function.__name__))
                print("To stop press Ctrl C")
            if(self.max_runs > 0 and self.runs >= self.max_runs):
                print("Closing: calling {0}".format(self.closefunc.__name__))
                self.closefunc()
                print("Closed: called {0} succesfully".format(self.closefunc.__name__))
                self.stop()
                break
            


    @property
    def _time(self):
        return self.interval - ((time.time() - self.start) % self.interval)

    def stop(self):
        self.event.set()
        #self.thread.join()
        #agilent.close()
        #update config file
        configParser.set('Output Settings', 'next_out', '{0}'.format(next_out+1))
        with open(config_file, 'w') as configfile:
            configParser.write(configfile)

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
#outline of the code:
# 1. create a visa resource manager
# 2. initializes communication with the agilent sa
# 3. set marker at modulation frequency
# 4. read periodically (t) the power of such peak from the marker using

#rm.list_resources()

#global variables:
#-----------------------------------

#variables:

period_meas = 0.6#in seconds for the ram
period_meas_temp = 15 #period for temp
number_meas = 24100 #number of measures
number_meas_temp = m.ceil(period_meas/period_meas_temp*number_meas)
print("Measuring {0} temperature data points".format(number_meas_temp))

out_path = "C:\\Users\\admin\Documents\\agilent\\data RAM\\data_{0}.txt"
temp_path = "C:\\Users\\admin\Documents\\agilent\\data RAM\\temp_{0}.txt"
config_file = "C:\\Users\\admin\Documents\\agilent\\data RAM\\config.txt"

configParser = configparser.RawConfigParser()   
configParser.read(config_file)

next_out = int(configParser.get('Output Settings', 'next_out'))
out_path = out_path.format(next_out)
temp_path = temp_path.format(next_out)

ref_level = -47 #in dBm
scale = 7 #in dBm per Div
span_unit = FreqUnit(FreqUnit.MHz) #1 = Mhz; 2 = kHz; 3 =GHz
span = 2 #in unit defined above
modulation_unit = FreqUnit(FreqUnit.MHz)
modulation_freq = 21 #in unit defined above
noise_h = 21.5
noise_l = 20.5
#agilent sa identifier:
#to find the identifier use the NI MAX, if connected with ethernet : Network devices and find visa ressource name, otherwise create a new one
identifier = "TCPIP0::10.118.16.12::inst0::INSTR"
dc_chan_scope = 2
#-------------------------
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
#----------------------
#prepare commands: (format the ones that need it)
ref_level_command =  ref_level_command.format(ref_level)
scale_command = scale_command.format(scale)
span_command = span_command.format(span, span_unit)
center_command = center_command.format(modulation_freq, modulation_unit)



#----------------------
#main program

#open resource:

        
        


def initialize_agilent():
    agilent = rm.open_resource(identifier)

    #setup:
    #--------------------------
    #set on sa
    agilent.write(sa)
    #set the span and center of the window
    agilent.write(span_command)
    agilent.write(center_command)
    #set y axis
    agilent.write(ref_level_command)
    agilent.write(scale_command)
    #set marker
    agilent.write(marker_on.format(1))
    agilent.write(marker_on.format(2))
    #agilent.write(marker_on.format(3))

    agilent.write(marker_command.format(1,modulation_freq, modulation_unit))
    agilent.write(marker_command.format(2,noise_h, modulation_unit))
    #agilent.write(marker_command.format(3,noise_l, modulation_unit))
    return agilent
    #---------------------

#initialize termo
T = Temperature(0,TempUnit(TempUnit.Celsius), datetime.now())
tem1 = Thermometer('COM9', 9600, 3)
#initialize scope
scope = Tecktronix2000("USB0::0x0699::0x036A::C101658::INSTR")
scope.open()
scope.setup_meas_avg(dc_chan_scope)
with open(out_path, 'w') as outfile:
    #sets headers and empty file:
        dc = scope.meas_avg(dc_chan_scope)
        T = tem1.readTemp()
        outfile.write("Time Period\t{0:.3f} \nMeasurements\t {1}\n".format(period_meas, number_meas))
        outfile.write("Time (s)\t RAM (dBm)\t Noise Level Right Side (+0.5 MHz) (dBm)\t DC Level ({0})\n".format(dc.unit))
with open(temp_path, 'w') as tempfile:
    T = tem1.readTemp()
    
    tempfile.write("Time Period\t{0:.3f} \nMeasurements\t {1}\n Temperature Unit\t{2}\n".format(period_meas_temp, number_meas_temp, T.unit))
    tempfile.write("Time (s)\t Temperature ({0})\n".format(T.unit))



#timer loop


def meas_loop(path, agilent: visa.Resource, scope: Tecktronix2000, ch: int):
    with open(path, 'a') as outfile:
        #in real change 25 to T.value
        T1 = datetime.now()
        RAM = agilent.query_ascii_values(marker_query.format(1))[0]
        NoiseH = agilent.query_ascii_values(marker_query.format(2))[0]
        dc = scope.meas_avg(ch) #Voltage(5, VoltUnit("V")) #
        #NoiseL = agilent.query_ascii_values(marker_query.format(3))[0]
        outfile.write("{0:.2f}\t{1:.3f}\t{2:.3f}\t{3:.6e}\n".format(dc.time.timestamp()-T0.timestamp(), RAM , NoiseH, dc.value))
def temp_meas(path):
    T1 = tem1.readTemp()
    
    #print("Temperature measured at {0}".format(datetime.now().strftime("%H:%M:%S.%f")))
    with open(path, 'a') as outfile:
        outfile.write("{0:.2f}\t{1:.1f}\n".format(T1.time.timestamp()-T0.timestamp(), T1.value))

agilent = initialize_agilent()
def close_fast_connections():
    agilent.close()
    scope.close()
def close_temp():
    tem1.close()
#start time:
T0 = datetime.now()
rt = RepeatedTimer(period_meas, number_meas, meas_loop, close_fast_connections, out_path, agilent, scope, dc_chan_scope)
rt_2 = RepeatedTimer(period_meas_temp, number_meas_temp, temp_meas, close_temp, temp_path)
#close resource
#agilent.close()
