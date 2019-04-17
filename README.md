# agilent_visa_control
A set of files aimed at facilitating the transfer of data from Agilent Spectrum Analizers through VISA Interface

## Prerequisites:

You will need PyVisa (and PyVisa's dependencies too obviously).

## Installation:

Just run:

```
pip install agilent-visa-control
```

For a good example on how to use the code check Agilent_save_trace.py in the bin folder.

Frequency.py is a helper class to help you deal with frequencies and its conversion. You can by using this class just sum or substract frequencies and the units will be taken care of by the script. You can then convert to which ever frequency unit you need. Check Frequency.py for examples on usage (after  `` if __name__ == __main__: ``)

## Usage of Agilent class:

Before using this class you will need to know the VISA identifier of the Agilent Spectrum Analyzer you'll want to use.
The identifier is usually found on the IO Librairies Suite of KeySight (https://www.keysight.com/en/pd-1985909/io-libraries-suite) (This suite is usually needed for communication with the Spectrum Analyzer) or in the instrument panel of your VISA package.

It is something like 
```python
identifier = "GPIB0::8::INSTR"
```
Import your library:
```
import agilent_visa_control.agilent as ag
```
Once you know your identifier you will need to create the Agilent class object:

```python
agilent = ag.Agilent(identifier)
```
Then you need to open your connection:
```python
agilent.open()
```

Then you could set the mode of the Analyzer, for example you could choose the spectrum analyzer mode. As of today the code only supports setting this mode remotely. You could always set in some other mode using the Frontal Interface on the instrument and then carry on extracting the data with this library.

```
agilent.set_sa()
```
Then you create the frequencies at which you want to center and the span of the analyzer.
```
center_freq = ag.Frequency(80.1, ag.FreqUnit(ag.FreqUnit.MHz))
span = ag.Frequency(50, ag.FreqUnit(ag.FreqUnit.kHz))
```
And we set the x Axis:
```
agilent.set_x(center_freq, span)
```
We set the Y axis now:
```python
agilent.set_y(3, 10) #in dBm (first argument is the reference Level and the second one is the scale in dBm per Div.
```
You can also set markers:
```
agilent.set_marker(1, center_freq)
```
And in the end we extract the values:
```python
values = agilent.get_trace(1)
#treat values
```
And in the end we close the connection.
```
#close connection once you are done with the agilent Spectrum Analyzer
agilent.close()
```
