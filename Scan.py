# https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window/

import PIL.Image, PIL.ImageTk, cv2, json, time, os
import numpy as np
import tkinter as tk

def rotate_bound(image, angle):
	# grab the dimensions of the image and then determine the
	# center
	(h, w) = image.shape[:2]
	(cX, cY) = (w // 2, h // 2)

	# grab the rotation matrix (applying the negative of the
	# angle to rotate clockwise), then grab the sine and cosine
	# (i.e., the rotation components of the matrix)
	M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
	cos = np.abs(M[0, 0])
	sin = np.abs(M[0, 1])

	# compute the new bounding dimensions of the image
	nW = int((h * sin) + (w * cos))
	nH = int((h * cos) + (w * sin))
 
	# adjust the rotation matrix to take into account translation
	M[0, 2] += (nW / 2) - cX
	M[1, 2] += (nH / 2) - cY

	# perform the actual rotation and return the image
	return cv2.warpAffine(image, M, (nW, nH))

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
			os.chdir('Processes')
			filename=os.getcwd() + os.path.sep + self.process+'.json'
		else:
			filename=self.path + os.path.sep + self.process+'.json'
		try:
			with open(filename) as f:
				process=json.loads(f.read())
		except:	
			process=None
			print("Fejl. Filen findes ikke:" + filename)
			
		os.chdir('..'+os.path.sep)
	
		self.process_name=process['process'][0]['meta']['name']
		self.process_description=process['process'][0]['meta']['description']
		self.merge_documents=process['process'][0]['meta']['merge_documents']
		self.AllowComment=process['process'][0]['meta']['AllowComment']
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

class App:
	def __init__(self, window, window_title, processes, video_source=0):
		self.window = window
		self.window.title(window_title)
		self.processes=processes
		self.video_source = video_source
		self.window.geometry("926x594")
		
		# open video source (by default this will try to open the computer webcam)
		self.vid = MyVideoCapture(self.video_source)
		#self.vid= rotate_bound(self.vid,90)		
		#Create the first label
		self.lb_process_var=tk.StringVar()
		self.lb_process = tk.Label(window, textvariable=self.lb_process_var)
		self.lb_process_var.set("Vælg proces: ")
		
		def ok(sl_process_var):
			print(type(self.sl_process_var))
			myProcess=sc_process(self.sl_process_var.get())
			print(myProcess)
			print(myProcess.getProcess_name() + ": " + myProcess.getProcess_desc())
			self.ms_process_var.set(myProcess.getProcess_name() + ": " + myProcess.getProcess_desc())

		#Create the selectbox for processes
		self.sl_process_var = tk.StringVar()
		self.sl_process_var.set("-vælg-") # default value
		self.sl_process = tk.OptionMenu(window, self.sl_process_var, *self.processes, command=ok)
		
		#Create the information area as message
		self.ms_process_var=tk.StringVar()
		#TOTO: Change this later
		self.ms_process = tk.Message(window, textvariable=self.ms_process_var, bg="white", width=350, anchor=tk.NW) 
		self.ms_process_var.set('Vælg scanningsproces i listen til venstre.')
		
		#Create the label for identification
		self.tx_cpr_var=tk.StringVar()
		self.tx_cpr=tk.Entry(window, textvariable=self.tx_cpr_var)
		self.img_previw_var=tk.StringVar()
		
		#Create the field for identification
		self.lb_cpr_var=tk.StringVar()
		self.lb_cpr_var.set("CPR: ")
		self.lb_cpr=tk.Label(window, textvariable=self.lb_cpr_var)
		
		# Create a canvas that can fit the above video source size
		self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
		#--->	self.canvas.pack()
		
		self.lb_process_step_var=tk.StringVar()
		self.lb_process_step=tk.Label(window, textvariable=self.lb_process_step_var)
		#TODO: Must be changed later
		self.lb_process_step_var.set("Scanner dokument 1 side 2")
	
		self.lb_comment_var=tk.StringVar()
		self.lb_comment=tk.Label(window, textvariable=self.lb_comment_var)
		self.lb_comment_var.set("Evt. bemærkning:")
	
		self.tx_comment_var=tk.StringVar()
		self.tx_comment=tk.Text(window, height=4, width=30)
		
		self.lb_status_var=tk.StringVar()
		self.lb_status=tk.Label(window,textvariable=self.lb_status_var, bg="darkgrey")
		self.lb_status_var.set("Status:")

		# Button that lets the user take a snapshot
		self.btn_snapshot=tk.Button(window, text="Scan", command=self.snapshot)
		#--->	self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)
		
		def skip():
			print("skip")
			#TODO: Must be done later
			
		def cancel():
			print("Afbryd")
			self.window.destroy()
		
		self.btn_skip=tk.Button(window,text="Skip", command=skip)
		self.btn_cancel=tk.Button(window,text="Afbryd", command=cancel)
		
		self.lb_process.grid(column=0, row=0, sticky=tk.N)
		self.sl_process.grid(column=1, row=0, sticky=tk.N)
		self.ms_process.grid(column=2, row=0, rowspan=2, sticky=tk.N+tk.S)
		self.lb_cpr.grid(column=0, row=1)
		self.tx_cpr.grid(column=1, row=1)
		self.canvas.grid(column=0, row=2, columnspan=2, rowspan=3, sticky=tk.W+tk.E)
		self.lb_process_step.grid(column=2, row=2, sticky=tk.NW)
		self.lb_comment.grid(column=2, row=3, sticky=tk.SW)
		self.tx_comment.grid(column=2, row=4, sticky=tk.NW)
		self.btn_snapshot.grid(column=2, row=5, sticky=tk.SW)
		self.btn_skip.grid(column=2, row=5, sticky=tk.S)
		self.btn_cancel.grid(column=2, row=5, sticky=tk.SE)
		self.lb_status.grid(column=0, columnspan=3, row=6, sticky=tk.W)

		# After it is called once, the update method will be automatically called every delay milliseconds
		self.delay = 30
		self.update()

		self.window.mainloop()

	def snapshot(self):
		self.lb_status_var.set("Status: Scanner...")
		
		# Get a frame from the video source
		ret, frame = self.vid.get_frame()


		if ret:
			frame = rotate_bound(frame,90)
			cv2.imwrite("tmp/frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".png", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

	def update(self):
		# Get a frame from the video source
		ret, frame = self.vid.get_frame()

		if ret:
			self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
			self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)

		self.window.after(self.delay, self.update)


class MyVideoCapture:
	def __init__(self, video_source=0):
		# Open the video source
		self.vid = cv2.VideoCapture(video_source)
		if not self.vid.isOpened():
			raise ValueError("Unable to open video source", video_source)

		# Get video source width and height
		#self.vid.set(cv2.VideoCapture.CV_CAP_PROP_FRAME_WIDTH, 1280)
		#self.vid.set(cv2.VideoCapture.CV_CAP_PROP_FRAME_HEIGHT, 720)
		self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
		self.shape = (self.width, self.height)

	def get_frame(self):
		if self.vid.isOpened():
			ret, frame = self.vid.read()
			if ret:
				# Return a boolean success flag and the current frame converted to BGR
				return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
			else:
				return (ret, None)
		else:
			return (ret, None)

	# Release the video source when the object is destroyed
	def __del__(self):
		if self.vid.isOpened():
			self.vid.release()

# Create a window and pass it to the Application object
processes=get_processes()
tmp_folder=os.getcwd() + os.path.sep +"tmp/"
cleanup_temp(tmp_folder)		
App(tk.Tk(), "Scan dokumenter", processes)
