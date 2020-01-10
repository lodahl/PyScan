#!/usr/bin/python3
import tkinter as tk


def open_dialog(processes):

	dialog = tk.Tk()
	dialog.title("Skan dokumenter")
	#Top frame
	topframe=tk.Frame(dialog, height=75, width=600)
	topframe.pack(side=tk.TOP, fill=tk.X)
	label_txt=tk.StringVar()
	process_label = tk.Label(topframe, textvariable=label_txt)
	label_txt.set("Vælg proces: ")
	process_label.pack(side=tk.LEFT, fill=tk.X)
	variable = tk.StringVar(topframe)
	#variable.set(processes[0]) # default value

	process_select = tk.OptionMenu(topframe, variable, *processes)
	process_select.pack(side=tk.LEFT)
	
	def cancel():
		print("Close")
		dialog.destroy()
	
	def ok():
		print ("value is:" + variable.get())
	
	#Center frame
	centerframe=tk.Frame(dialog, height=300, width=600, bg="lightgrey")
	
	#Buttom frame
	buttomframe=tk.Frame(dialog, height=75, width=600, bg="grey")
	ok_button = tk.Button(buttomframe, text="OK", command=ok)
	cancel_button = tk.Button(buttomframe, text="Afbryd", command=cancel)
	ok_button.pack(side=tk.LEFT)
	cancel_button.pack(side=tk.LEFT )
	
	centerframe.pack()
	buttomframe.pack()
	
	
	dialog.mainloop()


open_dialog(["test1", "Test2"])
