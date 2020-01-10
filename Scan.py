#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 20:35:31 2020

@author: leif
"""
import os, tkinter as tk, json
from PIL import ImageTk, Image
from time import sleep

def cleanup_temp(path):
	'''
	Deletes all files in a folder.
	Takes a path as parameter
	'''
	if os.path.exists(path):
		files=os.listdir(path)
		for file in files:
			#print(file)
			os.remove(path+ os.path.sep + file)

def create_temp(path):
	'''
	If the temporary folder doesn't exist its created.
	Takes a path as parameter
	'''
	if not os.path.exists(path):
		os.makedirs(path)

class sc_process:
	'''
	Loads one process from json and extracts all paramters (in profress).
	Takes progress name as manadatory parameter and path as volounteer parameter (current librery is default)
	Returns global variables?
	'''
	def __init__(self, process, path=None):

		self.process = process
		self.path=path
		
	
		if self.path == None:
			#print(os.getcwd())
			os.chdir('Processes')
			filename=os.getcwd() + os.path.sep + self.process+'.json'
		else:
			filename=self.path + os.path.sep + self.process+'.json'
		try:
			#print(filename)
			with open(filename) as f:
				process=json.loads(f.read())
		except:	
			process=None
			print("Fejl. Filen findes ikke")
			
		os.chdir('..'+os.path.sep)
	
		self.process_name=process['process'][0]['meta']['name']
		self.process_description=process['process'][0]['meta']['description']
		self.merge_documents=process['process'][0]['meta']['merge_documents']
		self.delevery_type=process['process'][1]['delevery']['delevery_type']
		self.destination=process['process'][1]['delevery']['destination']
		self.KLe=process['process'][2]['sbsys']['KLe']
		self.SkabelonID=process['process'][2]['sbsys']['SkabelonID']
		self.documents=process['process'][3]['documents']
		
	def getProcess_name(self):
		return self.process_name
	
	def getProcess_desc(self):
		return self.process_description
	
	def getProcess_merge_documents(self):
		return self.merge_documents
	
	def getdelevery_type(self):
		return self.delevery_type
	
	def getdestination(self):
		return self.destination
	
	def getKLe(self):
		return self.KLe
	
	def getSkabelonID(self):
		return self.SkabelonID
	
	def getdocuments(self):
		return self.documents

	def __str__(self):
		return "Process: " + self.process_name + " " + self.process_description

def get_processes(path=None):
	'''
	Get all the available processes from json files in folder.
	Cast path as parameter or leave blank for 'Processes' in current dir.
	Returns a list of strings.
	'''
	if path == None:
		os.chdir('Processes')
	else:
		os.chdir(path)
	process_files = [fn for fn in os.listdir()
		if any(fn.endswith(ext) for ext in ['json'])]
	processes=[]
	for file in process_files:
		process= file.split('.')[0]
		processes.append(process)
	os.chdir('..'+os.path.sep)

	return processes


def open_dialog(processes):
	'''
	This function runs the dialog
	'''
	dialog = tk.Tk()
	dialog.geometry("600x550")
	dialog.title("Skan dokumenter")
	
	lb_process_var=tk.StringVar()
	lb_process = tk.Label(dialog, textvariable=lb_process_var)
	lb_process_var.set("Vælg proces: ")
	
	tx_cpr_var=tk.StringVar()
	tx_cpr=tk.Entry(dialog, textvariable=tx_cpr_var)
	img_previw_var=tk.StringVar()	

	def ok(lb_process_var):
		myProcess=sc_process(lb_process_var)
		ms_process_var.set(myProcess.getProcess_name() + ": " + myProcess.getProcess_desc())

	sl_process_var = tk.StringVar()
	sl_process_var.set("-vælg-") # default value
	sl_process = tk.OptionMenu(dialog, sl_process_var, *processes, command=ok)

	ms_process_var=tk.StringVar()
	ms_process = tk.Message(dialog, textvariable=ms_process_var, bg="white",  width=350, anchor=tk.NW) #height=30,
	ms_process_var.set('                        ')

	lb_cpr_var=tk.StringVar()
	lb_cpr_var.set("CPR: ")
	lb_cpr=tk.Label(dialog, textvariable=lb_cpr_var)
   
	width = int(210*1.5)
	height =int(297*1.5)
	imgfile=os.getcwd()+os.path.sep+"dummy.png"
	print(imgfile)
	print(os.path.exists(imgfile))
	
	load = Image.open(imgfile)
	load = load.resize((width,height), Image.ANTIALIAS)
	render = ImageTk.PhotoImage(load)

	#img = Image.open(imgfile)
	#
	#image =  ImageTk.PhotoImage(img)
	lb_img_preview = tk.Label(dialog, image = render)  
	lb_img_preview.image = render
	lb_process_step_var=tk.StringVar()
	lb_process_step=tk.Label(dialog, textvariable=lb_process_step_var)
	lb_process_step_var.set("Scanner dokument 1 side 2")
	
	lb_comment_var=tk.StringVar()
	lb_comment=tk.Label(dialog, textvariable=lb_comment_var)
	lb_comment_var.set("Evt. bemærkning:")
	
	tx_comment_var=tk.StringVar()
	tx_comment=tk.Text(dialog, height=4, width=30)
	
	def scan():
		#ToDo Why doesn't this work?
		lb_status_var.set("Status: Scanner...")
		sleep(2)
		lb_status_var.set("Status: Færdig")
	
	btn_scan=tk.Button(dialog, text="Scan", command=scan)
	btn_skip=tk.Button(dialog,text="Skip")
	btn_cancel=tk.Button(dialog,text="Afbryd")
	
	lb_status_var=tk.StringVar()
	lb_status=tk.Label(dialog,textvariable=lb_status_var, bg="darkgrey")
	lb_status_var.set("Status:")
	
	def cancel():
		print("Close")
		dialog.destroy()

	btn_cancel = tk.Button(dialog, text="Afbryd", command=cancel)

	lb_process.grid(column=0, row=0, sticky=tk.N)
	sl_process.grid(column=1, row=0, sticky=tk.N)
	ms_process.grid(column=2, row=0, rowspan=2, sticky=tk.N+tk.S)
	lb_cpr.grid(column=0, row=1)
	tx_cpr.grid(column=1, row=1)
	lb_img_preview.grid(column=0, row=2, columnspan=2, rowspan=3, sticky=tk.W+tk.E)
	lb_process_step.grid(column=2, row=2, sticky=tk.NW)
	lb_comment.grid(column=2, row=3, sticky=tk.SW)
	tx_comment.grid(column=2, row=4, sticky=tk.NW)
	btn_scan.grid(column=2, row=5, sticky=tk.SW)
	btn_skip.grid(column=2, row=5, sticky=tk.S)
	btn_cancel.grid(column=2, row=5, sticky=tk.SE)
	lb_status.grid(column=0, columnspan=3, row=6, sticky=tk.W)
	
	dialog.mainloop()
	
#initializing
temp_path=os.getcwd()+'/tmp'
cleanup_temp(temp_path)
create_temp(temp_path)	


processes=get_processes()

open_dialog(processes)

'''
print(my_process)
print(my_process.getProcess_name())
print(my_process.getProcess_desc())
print(my_process.getProcess_merge_documents())
print(my_process.getdelevery_type())
print(my_process.getdestination())
print(my_process.getKLe())
print(my_process.getSkabelonID())
print(my_process.getdocuments())
'''
