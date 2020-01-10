#!/usr/bin/python3

import os, tkinter as tk
from PIL import ImageTk, Image
from time import sleep

def open_dialog(processes):
	'''
	This function runs the dialog
	'''
	dialog = tk.Tk()
	dialog.title("Skan dokumenter")
	
	lb_process_var=tk.StringVar()
	lb_process = tk.Label(dialog, textvariable=lb_process_var)
	lb_process_var.set("Vælg proces: ")
	
	tx_cpr_var=tk.StringVar()
	tx_cpr=tk.Entry(textvariable=tx_cpr_var)
	img_previw_var=tk.StringVar()	

	def ok(lb_process_var):
		print ("value is:" + lb_process_var)

	sl_process_var = tk.StringVar()
	sl_process_var.set("-vælg-") # default value
	sl_process = tk.OptionMenu(dialog, sl_process_var, *processes, command=ok)

	ms_process_var=tk.StringVar()
	ms_process = tk.Message(dialog, textvariable=ms_process_var, bg="white",  width=300) #height=30,
	ms_process_var.set("Lorem ipsum dolor sit amed du og jeg går en lang tur.")

	lb_cpr_var=tk.StringVar()
	lb_cpr_var.set("CPR: ")
	lb_cpr=tk.Label(dialog, textvariable=lb_cpr_var)
	

   
	width = int(210*1.5)
	height =int(297*1.5)
	#print(os.getcwd()+os.path.sep+"tmp/Skærmbillede.png")
	img = Image.open(os.getcwd()+os.path.sep+"tmp/Skærmbillede.png")
	img = img.resize((width,height), Image.ANTIALIAS)
	image =  ImageTk.PhotoImage(img)
	#image = tk.PhotoImage(photoImg)
    
	img_preview = tk.Label(dialog, textvariable=img_previw_var, image=image)
	img_previw_var.set("Forhåndsvisning")
	
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


	btn_ok = tk.Button(dialog, text="Vælg", command=ok)
	btn_cancel = tk.Button(dialog, text="Afbryd", command=cancel)

	lb_process.grid(column=0, row=0, sticky=tk.N)
	sl_process.grid(column=1, row=0, sticky=tk.N)
	ms_process.grid(column=2, row=0, rowspan=2, sticky=tk.N+tk.S)
	lb_cpr.grid(column=0, row=1)
	tx_cpr.grid(column=1, row=1)
	img_preview.grid(column=0, row=2, columnspan=2, rowspan=3, sticky=tk.W+tk.E)
	lb_process_step.grid(column=2, row=2, sticky=tk.NW)
	lb_comment.grid(column=2, row=3, sticky=tk.SW)
	tx_comment.grid(column=2, row=4, sticky=tk.NW)
	btn_scan.grid(column=2, row=5, sticky=tk.SW)
	btn_skip.grid(column=2, row=5, sticky=tk.S)
	btn_cancel.grid(column=2, row=5, sticky=tk.SE)
	lb_status.grid(column=0, columnspan=3, row=6, sticky=tk.W)
	
	dialog.mainloop()

processes=["Test 1", "Test 2"]
open_dialog(processes)
