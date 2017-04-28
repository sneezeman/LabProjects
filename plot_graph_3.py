from Tkinter import Tk, Button, StringVar, DoubleVar, Label, Entry, Frame
from tkFileDialog import askopenfilename
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

common_spike_list = []
number_in_seq = -1

# def make_sure_path_exists(path):
#     try:
#         os.makedirs(path)
#     except OSError as exception:
#         if exception.errno != errno.EEXIST:
#             raise

# def save_all():
# 	make_sure_path_exists('/'.join(data_file.split('/')[0:-1]))
# 	savefig()

def f_open():
	global data_file
	data_file = askopenfilename()
	data_path.set(data_file)

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
		tkMessageBox.showinfo('Most common spikes list', counter)

def next_common(forward):
	global number_in_seq
	most_common_spikes(False)
	if forward: 
		if number_in_seq < len(counter):
			number_in_seq = number_in_seq + 1
			main(counter[number_in_seq][0])
	else:
		if number_in_seq < 0:
			number_in_seq = number_in_seq + 1
			main(counter[number_in_seq][0])	
		if number_in_seq != 0:
			number_in_seq = number_in_seq - 1
			main(counter[number_in_seq][0])
	cell_number_plotted.set(counter[number_in_seq][0])
	plt.savefig(str(counter[number_in_seq][0]) + '.svg', bbox_inches='tight')
	

# plotting function: clear current, plot & redraw
def plot(theta, r, theta_s, r_s):
    plt.clf()
    ax = plt.subplot(111, projection='polar')
    ax.plot(theta, r, color = 'black', linewidth=0.3)
    #ax.plot(theta_s, r_s, marker='x', markersize=10, color = np.random.rand(3,1) ,linestyle = 'None')
    ax.plot(theta_s, r_s, marker='x', markersize=10, color = 'red' ,linestyle = 'None')
    plt.gcf().canvas.draw()
    toolbar.update()

def main(spike_number):
	cell_number_plotted.set('')
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

	plot(theta, r, theta_s, r_s)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
# GUI
root = Tk()
data_path = StringVar()
cell_number_plotted = StringVar()
data_path.set('First of all, open a file!')

Button(text='Open', command=f_open).pack()
Label(root, textvariable=data_path).pack()
Button(text='Most common spikes', command= lambda: most_common_spikes(True)).pack()
frame2 = Frame(root)
frame2.pack()
Label(frame2, text="Cell number: ").pack(side='left')
E1 = Entry(frame2, bd=5)
E1.pack(side='left')
Label(frame2, textvariable = cell_number_plotted).pack(side = 'left')
frame1 = Frame(root)
frame1.pack()
Button(frame1, text="Prev common", command = lambda: next_common(False)).pack(side='left')
Button(frame1, text="Plot!", command = lambda: main(E1.get())).pack(side='left')
Button(frame1, text="Next common", command = lambda: next_common(True)).pack(side='left')

# init figure
fig = plt.figure(figsize=(18, 16), dpi=80)
canvas = FigureCanvasTkAgg(fig, root)
toolbar = NavigationToolbar2TkAgg(canvas, root)
canvas.get_tk_widget().pack()
toolbar.pack()
toolbar.update()

Button(master=root, text='Quit', command=_quit).pack()
root.mainloop()