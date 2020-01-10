#!/usr/bin/python3
'''
Work in progress.
'''
import housekeeping, json, os, tkinter as tk

# Create all global variables first...
my_process_name=""
process_description=""
merge_documents=False
delevery_type=""
destination=""
KLe=""
SkabelonID=None
documents=[]

#Clean up temporary files
temp_path=os.getcwd()+'/tmp'
housekeeping.cleanup_temp(temp_path)
housekeeping.create_temp(temp_path)

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

def get_process(process_name, path=None):
	'''
	Loads one process from json and extracts all paramters (in profress).
	Takes progress name as manadatory parameter and path as volounteer parameter (current librery is default)
	Returns global variables?
	'''
	if path == None:
		#print(os.getcwd())
		os.chdir('Processes')
		filename=os.getcwd() + os.path.sep + process_name+'.json'
	else:
		filename=path + os.path.sep + process_name+'.json'
	try:
		#print(filename)
		with open(filename) as f:
			process=json.loads(f.read())
	except:
		process=None
		print("Fejl. Filen findes ikke")
	os.chdir('..'+os.path.sep)
	
	return process

def get_config(process):
	'''
	Extratcs paramters from json file.
	Takes process name as parameter
	Returns print (work in progress)
	'''
	global my_process_name, process_description, merge_documents, delevery_type, destination, KLe, SkabelonID, documents
	data=process
	my_process_name=data['process'][0]['meta']['name']
	process_description=data['process'][0]['meta']['description']
	merge_documents=data['process'][0]['meta']['merge_documents']
	delevery_type=data['process'][1]['delevery']['delevery_type']
	destination=data['process'][1]['delevery']['destination']
	KLe=data['process'][2]['sbsys']['KLe']
	SkabelonID=data['process'][2]['sbsys']['SkabelonID']
	documents=data['process'][3]['documents']


def open_dialog(processes):
	'''
	This function runs the dialog
	'''
	global process_description
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
	variable.set("-vælg-") # default value

	process_select = tk.OptionMenu(topframe, variable, *processes)
	process_select.pack(side=tk.LEFT)
	description_txt=tk.StringVar()
	description_label = tk.Label(topframe, textvariable=description_txt, bg="green")
	
	def cancel():
		print("Close")
		dialog.destroy()
	
	def ok():
		print ("value is:" + variable.get())
		process= get_process(variable.get())
		get_config(process)
		description_label.forget()

		description_txt.set(process_description)
		description_label.pack(side=tk.LEFT, fill=tk.X)
		print(process)
		print(process_description)

	ok_button = tk.Button(topframe, text="Vælg", command=ok)
	ok_button.pack(side=tk.LEFT)
	
	
	
	#Center frame
	centerframe=tk.Frame(dialog, height=300, width=600, bg="lightgrey")
	
	#Buttom frame
	buttomframe=tk.Frame(dialog, height=75, width=600, bg="grey")

	cancel_button = tk.Button(buttomframe, text="Afbryd", command=cancel)

	cancel_button.pack(side=tk.LEFT )
	
	centerframe.pack()
	buttomframe.pack()
	
	
	dialog.mainloop()





processes=get_processes()
open_dialog(processes)

#xprocess=get_process('process_2')


#config=get_config(xprocess)


print(my_process_name, process_description, merge_documents, delevery_type, destination, KLe, str(SkabelonID), documents)
