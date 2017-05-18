import matplotlib.pyplot as plt
import numpy as np

x_array = []
y_array = []
lineMassive = []

with open ('mhc.csv') as file:
	for line in file.readlines():
		lineMassive = line.split(';')
		x_array.append(float(lineMassive[1]))
		y_array.append(float(lineMassive[2]))

x_array_convolved = np.convolve(np.asarray(x_array), np.ones(5), mode='same')
y_array_convolved = np.convolve(np.asarray(y_array), np.ones(5), mode='same')

plt.plot(x_array_convolved, y_array_convolved)

#plt.title('About as simple as it gets, folks')
plt.grid(True)

plt.show()