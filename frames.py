
# frames.py
import tkinter
from PIL import ImageTk
from PIL import Image

class Frames:
    def __init__(self, mainObj, MainWin, wWidth, wHeight, function=0, Object=0, xAxis=10, yAxis=10):
        self.xAxis = xAxis
        self.yAxis = yAxis
        self.MainWindow = MainWin
        self.MainObj = mainObj
        self.method = function if function != 0 else None
        self.callingObj = Object if Object != 0 else None
        self.winFrame = tkinter.Frame(self.MainWindow, width=wWidth, height=wHeight)
        self.winFrame['borderwidth'] = 5
        self.winFrame['relief'] = 'ridge'
        self.winFrame.place(x=xAxis, y=yAxis)
        self.btnClose = tkinter.Button(self.winFrame, text="Close", width=8,
                                      command=lambda: self.quitProgram())
        self.btnClose.place(x=1020, y=600)
        self.btnView = tkinter.Button(self.winFrame, text="View", width=8,
                                      command=lambda: self.NextWindow())
        self.btnView.place(x=900, y=600)

    def setCallObject(self, obj):
        self.callingObj = obj

    def setMethod(self, function):
        self.method = function

    def quitProgram(self):
        self.MainWindow.destroy()

    def getFrames(self):
        return self.winFrame

    def unhide(self):
        self.winFrame.place(x=self.xAxis, y=self.yAxis)

    def hide(self):
        self.winFrame.place_forget()

    def NextWindow(self):
        listWF = list(self.MainObj.listOfWinFrame)
        if not self.method or not self.callingObj:
            print("Calling Method or the Object from which Method is called is None")
            return
        self.method()
        img = None
        if self.callingObj == self.MainObj.DT:
            img = self.MainObj.DT.getImage()
        else:
            print("Error: No specified object for getImage() function")
            return
        jpgImg = Image.fromarray(img)
        current = 0
        for i in range(len(listWF)):
            listWF[i].hide()
            if listWF[i] == self:
                current = i
        if current == len(listWF) - 1:
            listWF[current].unhide()
            listWF[current].readImage(jpgImg)
            listWF[current].displayImage()
            listWF[current].btnView['state'] = 'disabled'
        else:
            listWF[current + 1].unhide()
            listWF[current + 1].readImage(jpgImg)
            listWF[current + 1].displayImage()
        print("Step " + str(current) + " Extraction complete!")

    def readImage(self, img):
        self.image = img

    def displayImage(self):
        resized_img = self.image.resize((250, 250), Image.Resampling.LANCZOS)
        imgTk = ImageTk.PhotoImage(image=resized_img)
        if hasattr(self, 'labelImg'):
            self.labelImg.configure(image=imgTk)
            self.labelImg.image = imgTk
        else:
            self.labelImg = tkinter.Label(self.winFrame, image=imgTk)
            self.labelImg.place(x=700, y=150)