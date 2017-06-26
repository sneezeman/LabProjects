import numpy as np
from Tkinter import Tk, Button, StringVar, DoubleVar, Label, Entry, Frame, Checkbutton, BooleanVar, OptionMenu
from tkFileDialog import askopenfilename
import tkMessageBox
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from itertools import islice
import math


windowSize = 5
centerRadius = 10

def f_open():
	maxX = 0
	maxY = 0
	minX = 0
	minY = 0
	global matrixDimenstion
	global data_file
	data_file = askopenfilename()
	data_path.set(data_file)
	with open (data_file) as file:
		for line in islice(file, 1, None):
			lineMassive = line.split(';')
			if maxX < float(lineMassive[1]): maxX = float(lineMassive[1])
			if maxY < float(lineMassive[2]): maxY = float(lineMassive[2])
			if minX > float(lineMassive[1]): minX = float(lineMassive[1])
			if minY > float(lineMassive[2]): minY = float(lineMassive[2])
	matrixDimenstion = max(round(maxX) + round(abs(minX)), round(maxY) + round(abs(minY))) + 3
	if matrixDimenstion % 2 != 0: matrixDimenstion += 1
	print matrixDimenstion

def showTrajectory():

	x_array = []
	y_array = []
	lineMassive = []

	with open (data_file) as file:
		for line in islice(file, 1, None):
			lineMassive = line.split(';')
			x_array.append(float(lineMassive[1]))
			y_array.append(float(lineMassive[2]))

	x_array_convolved = np.convolve(np.asarray(x_array), np.ones(windowSize), mode='same')
	y_array_convolved = np.convolve(np.asarray(y_array), np.ones(windowSize), mode='same')

	#plt.plot(x_array, y_array)
	plt.plot([(i / windowSize) for i in x_array_convolved], [(i / windowSize) for i in y_array_convolved])
	plt.grid(True)

	plt.show()

def matrix(dims):

	x_array = []
	y_array = []
	lineMassive = []

	with open (data_file) as file:
		for line in islice(file, 1, None):
			lineMassive = line.split(';')
			x_array.append(float(lineMassive[1])/windowSize)
			y_array.append(float(lineMassive[2])/windowSize)
	
	x_array_convolved = np.convolve(np.asarray(x_array), np.ones(windowSize), mode='same')
	y_array_convolved = np.convolve(np.asarray(y_array), np.ones(windowSize), mode='same')

	global matrixGrid
	matrixGrid = np.zeros(dims)
	for i in range(len(x_array)): 
		matrixGrid[round(x_array_convolved[i]-matrixDimenstion/2), round(y_array_convolved[i]-matrixDimenstion/2)] = \
		matrixGrid[round(x_array_convolved[i]-matrixDimenstion/2), round(y_array_convolved[i]-matrixDimenstion/2)] + 1

	plt.matshow(matrixGrid)
	plt.show()

def addDataFile():

	x_array = []
	y_array = []
	lineMassive = []

	another_data_file = askopenfilename()
	data_path.set(data_path.get() + '\n' + another_data_file)

	with open (another_data_file) as file:
		for line in islice(file, 1, None):
			lineMassive = line.split(';')
			x_array.append(float(lineMassive[1])/windowSize)
			y_array.append(float(lineMassive[2])/windowSize)
	
	x_array_convolved = np.convolve(np.asarray(x_array), np.ones(windowSize), mode='same')
	y_array_convolved = np.convolve(np.asarray(y_array), np.ones(windowSize), mode='same')

	for i in range(len(x_array)): 
		matrixGrid[round(x_array_convolved[i]-matrixDimenstion/2), round(y_array_convolved[i]-matrixDimenstion/2)] = \
		matrixGrid[round(x_array_convolved[i]-matrixDimenstion/2), round(y_array_convolved[i]-matrixDimenstion/2)] + 1

	plt.matshow(matrixGrid)
	plt.show()

def cageParts():

	centerFrames = 0 
	quadrant1 = 0
	quadrant2 = 0
	quadrant3 = 0
	quadrant4 = 0

	x_array = []
	y_array = []
	lineMassive = []

	with open (data_file) as file:
		for line in islice(file, 1, None):
			lineMassive = line.split(';')
			x_array.append(float(lineMassive[1])/windowSize)
			y_array.append(float(lineMassive[2])/windowSize)
	
	x_array_convolved = np.convolve(np.asarray(x_array), np.ones(windowSize), mode='same')
	y_array_convolved = np.convolve(np.asarray(y_array), np.ones(windowSize), mode='same')

	for i in range(len(x_array)):
		if math.sqrt(x_array_convolved[i]**2 + y_array_convolved[i]**2) <= centerRadius:
			centerFrames += 1

	for i in range(len(x_array)):
		if x_array[i] > 0 and  y_array[i] > 0:
			quadrant1 += 1
		elif x_array[i] < 0 and  y_array[i] > 0:
			quadrant2 += 1
		elif x_array[i] < 0 and  y_array[i] < 0:
			quadrant3 += 1
		elif x_array[i] > 0 and  y_array[i] < 0:
			quadrant4 += 1


	tkMessageBox.showinfo('Stats', 'All frames: ' + str(len(x_array_convolved)) + '\n' + \
		'In center ' + str(centerRadius) + ' cm: ' + str(centerFrames) + '(~' + \
		str(round((float(centerFrames)/float(len(x_array_convolved))*100), 2)) + '%) \n' \
			+ 'Quadrants(1-2-3-4): \n' + str(round(float(quadrant1)/float(len(x_array_convolved)), 2)) + \
			'\n' + str(round(float(quadrant2)/float(len(x_array_convolved)), 2)) + '\n' + \
		str(round(float(quadrant3)/float(len(x_array_convolved)), 2)) + '\n' + \
		str(round(float(quadrant4)/float(len(x_array_convolved)), 2)))
	
root = Tk()
data_path = StringVar()
data_path.set('...')
Button(text='Open', command=f_open).pack()
Label(textvariable=data_path).pack()
Button(text='Trajectory', command=showTrajectory).pack()
Button(text='Matrix', command= lambda: matrix((matrixDimenstion, matrixDimenstion))).pack()
Button(text='Add another file to matrix', command=addDataFile).pack()
Button(text='Cage parts', command=cageParts).pack()
root.mainloop()