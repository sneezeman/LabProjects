from Tkinter import *
from tkFileDialog   import askopenfilename
from time import strftime
from itertools import islice
import math
import numpy as np

'''
# Delete after debug AND uncomment LINE 52
time_shift = 2.1
firstfile = 'Track-ca1_15-2-Trial     1-Arena 1-Subject 1.txt'
secondfile = 'spikes_CA1_15_2day_conc_recording_20161111_125551_corrected_neuropil_30.csv'

# UNCOMMENT LINE 52
'''

# Throw away elements exclude 10th
def every_tenth(massive):
	output = []
	for element in massive[::10]:
		output.append(element)
	return output

# Get 10 nearby elements
def ten_boys_form_hood(massive):
	stack = []
	i = 5
	for element in massive[5:-5:10]:
		stack.append(sum(massive[i-5:i+5])/10)
		i = i+10
	return stack

# Convolve with window from 10 elements
def ten_boys_form_hood2(massive):
	stack = np.convolve(np.asarray(massive), np.ones(10), mode='same')
	return stack.tolist()

# Crutches. Throw away first and last speed.
def fill_speed_with_none(massive):
	massive_out = []
	k = 0
	massive_out.append(None)
	for j in range(1, len(x_massive)-10):
		if j%10 == 0:
			massive_out.append(massive[k])
			k = k+1
		else:
			massive_out.append(None)
	return massive_out

# Buttons metods
def callback():
    global firstfile
    firstfile= askopenfilename()
    track_path.set(firstfile)

def callback2():
	global secondfile
	secondfile= askopenfilename()
	spikes_path.set(secondfile)

def close_window():
	global time_shift 
	time_shift = E1.get()
	master.destroy()

# Window disign
master = Tk()
master.geometry("800x200")
track_path = StringVar()
track_path.set('...')
spikes_path = StringVar()
spikes_path.set('...')
Button(text='Track', command=callback).pack(fill=X)
Label(master, textvariable=track_path).pack(fill=X)
Button(text='Spikes', command=callback2).pack(fill=X)
Label(master, textvariable=spikes_path).pack(fill=X)
L1 = Label(master, text="Time shift (VT. Example:12-2 23):")
L1.pack()
E1 = Entry(master, bd=5)
E1.pack()
Button(text='OK', command=close_window).pack(side = BOTTOM, fill=X)
mainloop()

# Set lists
time_massive = []
x_massive = []
y_massive = []
angle_massive = []
speed_massive = []
speed_massive_expanded = []
spikes_massive = []
temp_array = []
speed_from_file = []
speed_massive_alt = []
speed_massive_alt_expanded = []
speed_3 = []
speed_3_exp = []

# Get header lines number
with open(firstfile, 'rb') as inputfile:
	first_line = inputfile.readline()
	header_lines_number = float(first_line[-6:-4])
	delimeter = first_line[-3]

# Fill arrays with data
with open(firstfile, 'rb') as inputfile:
	for line in islice(inputfile, header_lines_number, None):
		line_massive = line.split(delimeter)
		if not line_massive[2].replace('.','').replace('-', '').isdigit():
			continue
		else:
			time_massive.append(float(line_massive[0]))
			x_massive.append(float(line_massive[2]))
			y_massive.append(float(line_massive[3]))
			try:
				speed_from_file.append(float(line_massive[8]))
			except ValueError:
				speed_from_file.append(0);
			angle_massive.append(180 + round((math.degrees(math.atan2(float(line_massive[3]), \
				float(line_massive[2])))),3))

# Fill speed array
for i in range(1, len(ten_boys_form_hood2(x_massive))):
	speed_massive_expanded.append(round(math.sqrt((ten_boys_form_hood2(x_massive)[i] - \
	ten_boys_form_hood2(x_massive)[i-1])**2 + (ten_boys_form_hood2(y_massive)[i] - \
	ten_boys_form_hood2(y_massive)[i-1])**2), 3))

# Fill array with None 
with open(secondfile, 'rb') as spikes:
	lines = spikes.readlines()
	for line in lines:
		line_array = []
		line_splitted = line.split(',')
		for row in line_splitted[1:]:
			if float(row) > 0:
				line_array.append(line_splitted.index(row))
		if not line_array:
			line_array.append(None)
		spikes_massive.append(str(line_array).strip("[]"))


# Time shife usage. Method 1 - create empty fields for track data
for m in range(int(round((time_massive[0]-float(time_shift))*20))):
	time_massive.insert(0, None)
	speed_massive_expanded.insert(0, None)
	angle_massive.insert(0, None)

# Time shife usage. Method 2 - ?
'''
for x in range(int(round((time_massive[0]-float(time_shift))*20))):
	line_array.insert(0, None)
'''

# Set output filename
filename = ('big_output ' + strftime('%d-%m-%Y %H:%M:%S') + '.csv')

# Creating output
with open (filename, 'w') as big_output:
	for i in range(len(time_massive)):
		try:
			big_output.write(str(time_massive[i]) +';' + str(angle_massive[i])+';' \
			 + str(speed_massive_expanded[i])+';'  + str(spikes_massive[i]).replace(" ", "") +';' +'\n')
		except IndexError:
			pass

print (str(len(time_massive) - len(spikes_massive)) + ' lines were not printed')