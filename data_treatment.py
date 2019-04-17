import matplotlib.pyplot as plt
import numpy as np

#files
masterpth = r"Z:\Lasers\L850P200\Agilent Code\data_mastermaster.txt"
slavepth = r"Z:\Lasers\L850P200\Agilent Code\data_masterslave.txt"
emipth = r"Z:\Lasers\L850P200\Agilent Code\data_emi.txt"
rampth = r"Z:\Lasers\L850P200\Agilent Code\data_ram.txt"

freqvals, mastervals = np.loadtxt(masterpth, unpack=True)
slavevals = np.loadtxt(slavepth, usecols=1, unpack=True)
emivals = np.loadtxt(emipth, usecols=1, unpack=True)
ramvals = np.loadtxt(rampth, usecols=1, unpack=True)

fig, ax = plt.subplots(figsize=(5,3))

ax.plot(freqvals, slavevals, label="Slave Laser Beat Note")
ax.plot(freqvals, mastervals, label="Master Laser Beat Note")
ax.plot(freqvals, emivals, label="emi Noise")
ax.plot(freqvals, ramvals, label="ram Noise")
ax.grid()
ax.legend()
plt.show()
