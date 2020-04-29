# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/

import tkinter as tk
from tkinter import filedialog
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np

LARGE_FONT= ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self, width=375, height=300)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Welcome to Pressure Analysis", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        

        button = tk.Button(self, text="Shoe Sensors",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = tk.Button(self, text="Crutch Sensor",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Shoe Sensor Analysis", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        uploadButton = tk.Button(self, text="Upload File",command= analyzeShoe)
        uploadButton.pack()
               
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Crutch Sensor",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Crutch Sensor Analysis", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        uploadButton = tk.Button(self, text="Upload File",command= analyzeCrutch)
        uploadButton.pack()
               

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Shoe Sensor",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()

    
def analyzeCrutch():
    root = Tk()
    mainFrame = Frame(root, width=300, height =300)
    mainFrame.pack()
    root.filename =  filedialog.askopenfilename(title = "Choose File")
    fileChosen = root.filename
    root.update()
    pullData = open(fileChosen,'r').read()
    dataArray = pullData.split('\n')
    time=[]
    force=[]
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            time.append(float(x))
            force.append(float(y))
    maxForce = max(force)
    maxLabel = Label(mainFrame, text = "Maximum Force Applied to Crutch is:", font = LARGE_FONT)
    maxLabel.pack(pady=10,padx=10)
    maxValLabel = Label(mainFrame, text = str(maxForce), font = LARGE_FONT)
    maxValLabel.pack(pady=10,padx=10)
    
    plt.plot(time,force)
    plt.show()
   
def analyzeShoe():
   root = Tk()
   mainFrame = Frame(root, width=300, height =300)
   mainFrame.pack()
   root.filename =  filedialog.askopenfilename(title = "Choose File")
   fileChosen = root.filename
   root.update()
   pullData = open(fileChosen,'r').read()
   dataArray = pullData.split('\n')
   time=[]
   frontForce=[]
   middleForce=[]
   backForce=[]
   for eachLine in dataArray:
       if len(eachLine)>1:
           t,x,y,z = eachLine.split(',')
           time.append(int(t))
           frontForce.append(float(x))
           middleForce.append(float(y))
           backForce.append(float(z))
           
   avgFForce = sum(frontForce)/len(frontForce)
   avgMForce = sum(middleForce)/len(middleForce)
   avgBForce = sum(backForce)/len(backForce)
   
   avgFLabel = Label(mainFrame, text = "Average Force Applied to the Toe Bone:", font = LARGE_FONT)
   avgFLabel.pack(pady=10,padx=10)
   avgFLabel2 = Label(mainFrame, text = str(avgFForce), font = LARGE_FONT)
   avgFLabel2.pack(pady=10,padx=10)
   
   avgMLabel = Label(mainFrame, text = "Average Force Applied to Mid-Foot:", font = LARGE_FONT)
   avgMLabel.pack(pady=10,padx=10)
   avgMLabel2 = Label(mainFrame, text = str(avgMForce), font = LARGE_FONT)
   avgMLabel2.pack(pady=10,padx=10)
   
   avgBLabel = Label(mainFrame, text = "Average Force Applied to the Heel:", font = LARGE_FONT)
   avgBLabel.pack(pady=10,padx=10)
   avgBLabel2 = Label(mainFrame, text = str(avgBForce), font = LARGE_FONT)
   avgBLabel2.pack(pady=10,padx=10)
   
   averages = []
   averages.append(avgFForce)
   averages.append(avgMForce)
   averages.append(avgBForce)
   
   pos = 0
   biggest = averages[0]
   for i in range(0, len(averages)):
        if(averages[i] > biggest):
            biggest = averages[i]
            pos = i
   if(pos == 0):
        result = Label(mainFrame, text = "Your Gait is Front Heavy: Most of the Pressure is on your toe bone", font = LARGE_FONT)
        result.pack(pady=10,padx=10)
   if(pos == 1):
        result = Label(mainFrame, text = "Your Gait is Even: Your step has equal distribution of weight", font = LARGE_FONT)
        result.pack(pady=10,padx=10)
   if(pos == 2):
        result = Label(mainFrame, text = "Your Gait is Back Heavy: Most of the Pressure is on your Heel", font = LARGE_FONT)
        result.pack(pady=10,padx=10)
   
   plt.plot(time,frontForce)
   plt.plot(time, middleForce)
   plt.plot(time,backForce)
   plt.show()
   
   
   

   
        
    




app = SeaofBTCapp()
app.mainloop()
