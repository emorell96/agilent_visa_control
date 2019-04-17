# agilent_visa_control
A set of files aimed at facilitating the transfer of data from Agilent Spectrum Analizers through VISA Interface

Prerequisites:

You will need PyVisa (and PyVisa's dependencies too obviously).

Installation:

No need to install, just clone this repository to your working workspace folder and code inside of it.

For a good example on how to use the code check Agilent_save_trace.py

Frequency.py is a helper class to help you deal with frequencies and its conversion. You can by using this class just sum or substract frequencies and the units will be taken care of by the script. You can then convert to which ever frequency unit you need. Check Frequency.py for examples on usage (after  `` if __name__ == __main__: ``)
