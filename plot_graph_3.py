from Tkinter import Tk, Button, StringVar, DoubleVar, Label, Entry, Frame, Checkbutton, BooleanVar, OptionMenu
from tkFileDialog import askopenfilename
from time import strftime
import tkMessageBox
import numpy as np
import matplotlib
import math
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import collections
import os
import errno

dirName = ('SvgPicFolder ' + strftime('%d-%m-%Y %H:%M:%S'))
common_spike_list = []
speedNormalized = []
number_in_seq = -1
cmap = plt.get_cmap('hot')


def f_open():
	global data_file
	global speedNormalized
	speedNormalized = []
	speed = []
	data_file = askopenfilename()
	data_path.set(data_file)
	most_common_spikes(False)
	with open(data_file, 'rb') as data:
		lines = data.readlines()
		for line in lines:
			line_massive = line.split(';')
			if line_massive[0] == 'None':
				continue
			else:
				speed.append(float(line_massive[2]))
	for i in range(len(speed)):
		speedNormalized.append(speed[i]/float(max(speed)))


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def saveFigure(cellNumber):
	make_sure_path_exists(dirName)
	plt.savefig(dirName + '/' + cellNumber + extention.get(), bbox_inches='tight', dpi = 400)

def most_common_spikes(from_button):
	global counter
	with open (data_file, 'rb') as spikes:
		lines = spikes.readlines()
		second_spikes_massive = []
		for line in lines:
			line_splitted = line.split(';')
			if line_splitted[0] == 'None':
				continue
			if line_splitted[3] != 'None':
				for k in line_splitted[3].split(','):
					second_spikes_massive.append(int(k));

	counter = collections.Counter(second_spikes_massive).most_common()

	if from_button:
		tkMessageBox.showinfo('Most common spikes list', 'Cell number, times \n' + str(counter).replace('[', '').replace(']',''))

def next_common(forward):
	global number_in_seq
	if forward: 
		if number_in_seq < len(counter)-1:
			number_in_seq = number_in_seq + 1
			main(counter[number_in_seq][0], False)
	else:
		if number_in_seq < 0:
			number_in_seq = number_in_seq + 1
			main(counter[number_in_seq][0], False)	
		if number_in_seq != 0:
			number_in_seq = number_in_seq - 1
			main(counter[number_in_seq][0], False)
	cellNumberChoosed.set(counter[number_in_seq][0])
	if bool_save.get():
		saveFigure(str(counter[number_in_seq][1]) + '-' + str(counter[number_in_seq][0]))
	

# plotting function: clear current, plot & redraw
def plot(theta, r, theta_s, r_s, speed):
    plt.clf()
    ax = plt.subplot(111, projection='polar')
    if boolSpeed.get():
    	for x in range(len(theta)-1):
    		ax.plot([theta[x], theta[x+1]],[r[x], r[x+1]], c = cmap(speed[x]), linewidth=0.7)
    else:
    	ax.plot(theta, r, color = 'black', linewidth=0.7)
    ax.plot(theta_s, r_s, marker='2', markersize=10, color = 'green' ,linestyle = 'None')
    plt.gcf().canvas.draw()
    firstPartOfName = 'clear plot'
    if bool_save.get():
    	for element in counter:
    		if int(element[0]) == int(E1.get()):
    			firstPartOfName = element[1]
    	if firstPartOfName == 'clear plot':
    		firstPartOfName = '0'
    	saveFigure(str(firstPartOfName) + '-' + E1.get())
    toolbar.update()

def plotAll(theta, r, theta_s, r_s, speed):
    if firstTime:
        plt.clf()
    ax = plt.subplot(111, projection='polar')
    if firstTime:
    	if boolSpeed.get():
    		for x in range(len(theta)-1):
    			ax.plot([theta[x], theta[x+1]],[r[x], r[x+1]], c = cmap(speed[x]), linewidth=0.7)
    	else:
        	ax.plot(theta, r, color = 'black', linewidth=0.7)
    
    ax.plot(theta_s, r_s, marker='x', markersize=10, color = np.random.rand(3,1) ,linestyle = 'None')
    plt.gcf().canvas.draw()
    toolbar.update()

def mainShowAll():
	global firstTime
	firstTime = True
	for pair in counter:
		main(pair[0], True)
		firstTime = False
	if bool_save.get():
		saveFigure('All spikes')

def main(spike_number, showAll):
	try:
		int(spike_number)
	except ValueError:
		spike_number = 0

	r = []
	theta = []
	r_s = []
	theta_s = []
	with open(data_file, 'rb') as data:
		lines = data.readlines()
		for line in lines:
			line_massive = line.split(';')
			if line_massive[0] == 'None':
				continue
			else:
				r.append(line_massive[0])
				theta.append(float(line_massive[1])*2*math.pi/360)

			if not line_massive[0] == 'None' and line_massive[3] != 'None':
				for k in line_massive[3].split(','):
					if float(k) == float(spike_number):
						r_s.append(line_massive[0])
						theta_s.append(float(line_massive[1])*2*math.pi/360)

	if showAll:
		plotAll(theta, r, theta_s, r_s, speedNormalized)
	else:
		plot(theta, r, theta_s, r_s, speedNormalized)


def saveAll(trashhold):
	try:
		int(trashhold)
	except ValueError:
		trashhold = 1
	most_common_spikes(False)
	for i in range(len(counter)):
		if counter[i][1] >= int(trashhold):
			main(counter[i][0], False)
			saveFigure(str(counter[i][1]) + '-' + str(counter[i][0]))

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
# GUI
root = Tk()
data_path = StringVar()
cellNumberChoosed = StringVar()
trashhold = StringVar()
trashhold.set(1)
bool_save = BooleanVar()
boolSpeed = BooleanVar()
data_path.set('First of all, open a file!')
extention = StringVar()
extention.set(".png") # default value


Button(text='Open', command=f_open).pack()
Label(root, textvariable=data_path).pack()
frame1 = Frame(root)
frame1.pack()
Button(frame1, text='Most common spikes list', command= lambda: most_common_spikes(True)).pack(side = 'left')
Button(frame1, text = "Show all spikes", command = lambda: mainShowAll()).pack(side = 'left')
frame2 = Frame(root)
frame2.pack()
Label(frame2, text="Cell number: ").pack(side='left')
E1 = Entry(frame2, textvariable = cellNumberChoosed, bd=5)
E1.pack(side='left')
Button(frame2, text="Plot!", command = lambda: main(E1.get(),False)).pack(side='left')
frame3 = Frame(root)
frame3.pack()
Button(frame3, text="Prev common", command = lambda: next_common(False)).pack(side='left')
Button(frame3, text="Next common", command = lambda: next_common(True)).pack(side='left')
Checkbutton(frame3, text="Save", variable = bool_save).pack(side='left')
Checkbutton(frame3, text="Speed (~7 min per cell)", variable = boolSpeed).pack(side='left')
frame4 = Frame(root)
frame4.pack()
Button(frame4, text = "Save all", command = lambda: saveAll(E2.get())).pack(side = 'left')
Label(frame4, text = "Trashold: ").pack(side='left')
E2 = Entry(frame4, textvariable = trashhold,bd = 5)
E2.pack(side = 'left')
w = OptionMenu(frame4, extention, ".png", ".svg")
w.pack()

# init figure
fig = plt.figure(dpi=80)
canvas = FigureCanvasTkAgg(fig, root)
toolbar = NavigationToolbar2TkAgg(canvas, root)
canvas.get_tk_widget().pack()
toolbar.pack()
toolbar.update()

Button(master=root, text='Quit', command=_quit).pack()
root.mainloop()