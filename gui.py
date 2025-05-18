import tkinter
from PIL import Image
from tkinter import filedialog
import cv2 as cv
from frames import *
from displayTumor import *
from predictTumor import *


class Gui:
    MainWindow = 0
    listOfWinFrame = list()
    FirstFrame = object()
    val = 0
    fileName = 0
    DT = object()

    wHeight = 700
    wWidth = 1180

    def __init__(self):
        global MainWindow
        MainWindow = tkinter.Tk()
        MainWindow.geometry('1200x720')
        MainWindow.resizable(width=False, height=False)

        self.DT = DisplayTumor()

        self.fileName = tkinter.StringVar()

        self.FirstFrame = Frames(self, MainWindow, self.wWidth, self.wHeight, 0, 0)
        self.FirstFrame.btnView['state'] = 'disable'

        self.listOfWinFrame.append(self.FirstFrame)

        WindowLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Brain Tumor Detection", height=1, width=40)
        WindowLabel.place(x=320, y=30)
        WindowLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"))

        self.val = tkinter.IntVar()
        RB1 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="Detect Tumor", variable=self.val,
                                  value=1, command=self.check)
        RB1.place(x=250, y=200)
        RB2 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="View Tumor Region",
                                  variable=self.val, value=2, command=self.check)
        RB2.place(x=250, y=250)

        browseBtn = tkinter.Button(self.FirstFrame.getFrames(), text="Browse", width=8, command=self.browseWindow)
        browseBtn.place(x=800, y=550)

        MainWindow.mainloop()

    def getListOfWinFrame(self):
        return self.listOfWinFrame


    def browseWindow(self):
        FILEOPENOPTIONS = dict(
            defaultextension='*.*',
            filetypes=[
                ('jpg', '*.jpg'),
                ('png', '*.png'),
                ('jpeg', '*.jpeg'),
                ('All Files', '*.*')
            ]
        )
        # open file dialog and get selected path
        self.fileName = filedialog.askopenfilename(**FILEOPENOPTIONS)
        if not self.fileName:
            return  # user cancelled

        # load PIL image for display
        pil_img = Image.open(self.fileName)
        self.listOfWinFrame[0].readImage(pil_img)
        self.listOfWinFrame[0].displayImage()

        # also keep an OpenCV copy for prediction
        self.mriImage = cv.imread(self.fileName, cv.IMREAD_COLOR)

        # pass PIL image to DisplayTumor object
        self.DT.readImage(pil_img)


    def check(self):
        # make sure an image has been loaded
        if not hasattr(self, 'mriImage'):
            tkinter.messagebox.showerror("Error", "Please browse and load an image first.")
            return

        choice = self.val.get()
        if choice == 1:
            # Tumor detection
            self.listOfWinFrame = [self.FirstFrame]
            self.listOfWinFrame[0].setCallObject(self.DT)

            prob = predictTumor(self.mriImage)
            txt = "Tumor Detected" if prob > 0.5 else "No Tumor"
            color = "red" if prob > 0.5 else "green"

            resLabel = tkinter.Label(
                self.FirstFrame.getFrames(),
                text=txt,
                height=1,
                width=20,
                fg=color,
                font=("Comic Sans MS", 16, "bold"),
                background="White"
            )
            resLabel.place(x=700, y=450)

        elif choice == 2:
            # View tumor region
            self.listOfWinFrame = [self.FirstFrame]
            self.listOfWinFrame[0].setCallObject(self.DT)
            self.listOfWinFrame[0].setMethod(self.DT.removeNoise)

            secFrame = Frames(
                self,
                MainWindow,
                self.wWidth,
                self.wHeight,
                self.DT.displayTumor,
                self.DT
            )
            self.listOfWinFrame.append(secFrame)

            # hide all but the first frame
            for i, frame in enumerate(self.listOfWinFrame):
                if i != 0:
                    frame.hide()
            self.listOfWinFrame[0].unhide()

            # enable the "View" button
            if len(self.listOfWinFrame) > 1:
                self.listOfWinFrame[0].btnView['state'] = 'active'

        else:
            # no valid option selected
            tkinter.messagebox.showinfo("Info", "Please select an option first.")


mainObj = Gui()