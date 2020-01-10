#import PIL
from PIL import Image
from PIL import ImageTk
import tkinter as tk, os
#print(dir(Image))

dialog = tk.Tk()

myfile=os.getcwd()+os.path.sep+"tmp/img_test.png" #Søndervig.jpg"

img = tk.PhotoImage(file=myfile)

#img = tk.PhotoImage(file=os.getcwd()+os.path.sep+"tmp/img_test.png")

img_preview = tk.Label(dialog, image=img)
img_preview.pack()


dialog.mainloop()


'''
    img = Image.open(x)
    img = img.resize((250, 250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(root, image=img)
    panel.image = img
    panel.pack()
    
   
	image = tk.PhotoImage(file=os.getcwd()+os.path.sep+"tmp/Søndervig.jpg")
	img_preview = tk.Label(textvariable=img_previw_var, image=image)
'''
