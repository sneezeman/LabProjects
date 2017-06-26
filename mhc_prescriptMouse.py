from Tkinter import *
from tkFileDialog   import askopenfilename
from time import strftime
import pandas as pd
from itertools import islice
import math
import numpy as np

# Set output filename 
filename = ('mhc_outputMouse ' + strftime('%d-%m-%Y %H:%M:%S') + '.csv')
dataStart = 0;

def callback():
    global firstfile
    firstfile= askopenfilename()
    firstMarkerFilePath.set(firstfile)

def getHeaderLinesNumber(filename):
	with open(filename, 'rb') as inputfile:
		first_line = inputfile.readline()
		header_lines_number = float(first_line[-6:-4])
	return header_lines_number

def getData(filename):
	global dataStart
	time_massive = []
	x_massive = []
	y_massive = []
	angle_massive = []
	header_lines_number = getHeaderLinesNumber(filename)
	with open(filename, 'rb') as inputfile:
		for line in islice(inputfile, header_lines_number, None):
			line_massive = line.split(';')
			if not line_massive[2].replace('.','').replace('-', '').isdigit():
				time_massive.append(float(line_massive[0]))
				x_massive.append(float(line_massive[2]))
				y_massive.append(float(line_massive[3]))
				angle_massive.append(360 + round((math.degrees(math.atan2(float(line_massive[3]), \
				float(line_massive[2])))),3))

	return time_massive, x_massive, y_massive, angle_massive

def go():

	firstArray = getData(firstfile);

	for i in range(len(firstArray[1])-1):
		outputTimeArray.append(firstArray[0][i]);
		outputXArray.append(round(firstArray[1][i],2));
		outputYArray.append(round(firstArray[2][i],2));
		outputAngleArray.append(360 - (firstArray[3][i]));
	master.destroy()

	# Creating output
	with open (filename, 'w') as mhc_output:
		mhc_output.write("\"Number of header lines:\",\"1\","+'\n')
		for i in range(len(outputTimeArray)):
			mhc_output.write(str(outputTimeArray[i]) +';' + str(outputXArray[i])+';' \
			 + str(outputYArray[i])+';'  + str(outputAngleArray[i]) +';' +'\n')

# Window disign
master = Tk()
master.geometry("500x300")
firstMarkerFilePath = StringVar()
firstMarkerFilePath.set('...')

Button(text='Mouse data file', command=callback).pack(fill=X)
Label(master, textvariable=firstMarkerFilePath).pack(fill=X)

Button(text='OK', command=go).pack(side = BOTTOM, fill=X)
mainloop()
