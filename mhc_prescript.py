from Tkinter import *
from tkFileDialog   import askopenfilename
from time import strftime
import pandas as pd
from itertools import islice
import math
import numpy as np

# Set output filename 
filename = ('mhc_output ' + strftime('%d-%m-%Y %H:%M:%S') + '.csv')
dataStart = 0;

def callback():
    global firstfile
    firstfile= askopenfilename()
    firstMarkerFilePath.set(firstfile)

def callback2():
	global secondfile
	secondfile= askopenfilename()
	secondMarkerFilePath.set(secondfile)

def callback3():
	global thirdfile
	thirdfile= askopenfilename()
	thirdMarkerFilePath.set(thirdfile)

def getHeaderLinesNumber(filename):
	with open(filename, 'rb') as inputfile:
		first_line = inputfile.readline()
		header_lines_number = float(first_line[-6:-4])
	return header_lines_number

def getData(filename, fristExecution):
	global dataStart
	time_massive = []
	x_massive = []
	y_massive = []
	angle_massive = []
	header_lines_number = getHeaderLinesNumber(filename)
	with open(filename, 'rb') as inputfile:
		for line in islice(inputfile, header_lines_number, None):
			line_massive = line.split(';')
			if fristExecution:
				if not line_massive[2].replace('.','').replace('-', '').isdigit():
					continue
				else:
					if line_massive[0] > dataStart:
						dataStart = line_massive[0];
					break
			else:
				if line_massive[0] < dataStart:
					continue
				else:
					try:
						time_massive.append(float(line_massive[0]))
						x_massive.append(float(line_massive[2]))
						y_massive.append(float(line_massive[3]))
						angle_massive.append(360 + round((math.degrees(math.atan2(float(line_massive[3]), \
							float(line_massive[2])))),3))
					except ValueError:
						pass

	return time_massive, x_massive, y_massive, angle_massive

def go():

	firstArray = getData(firstfile, True);
	secondArray = getData(secondfile, True);
	thirdArray = getData(thirdfile, True);

	firstArray = getData(firstfile, False);
	secondArray = getData(secondfile, False);
	thirdArray = getData(thirdfile, False);

	global outputTimeArray 
	global outputXArray
	global outputYArray
	global outputAngleArray 

	outputTimeArray = []
	outputXArray = []
	outputYArray = []
	outputAngleArray = []

	# print len(firstArray[1])
	# print len(secondArray[1])
	# print len(thirdArray[1])

	for i in range(min(len(firstArray[1])-1, len(secondArray[1])-1, len(thirdArray[1])-1)):
		outputTimeArray.append(firstArray[0][i]);
		outputXArray.append(0-round((firstArray[1][i] + secondArray[1][i]+ thirdArray[1][i])/3,2));
		outputYArray.append(0-round((firstArray[2][i] + secondArray[2][i]+ thirdArray[2][i])/3,2));
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
master.geometry("800x300")
firstMarkerFilePath = StringVar()
firstMarkerFilePath.set('...')
secondMarkerFilePath = StringVar()
secondMarkerFilePath.set('...')
thirdMarkerFilePath = StringVar()
thirdMarkerFilePath.set('...')
Button(text='First marker data file', command=callback).pack(fill=X)
Label(master, textvariable=firstMarkerFilePath).pack(fill=X)
Button(text='Second marker data file', command=callback2).pack(fill=X)
Label(master, textvariable=secondMarkerFilePath).pack(fill=X)
Button(text='Third marker data file', command=callback3).pack(fill=X)
Label(master, textvariable=thirdMarkerFilePath).pack(fill=X)
Button(text='OK', command=go).pack(side = BOTTOM, fill=X)
mainloop()
