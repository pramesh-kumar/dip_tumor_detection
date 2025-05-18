
# gui.py
import tkinter
from tkinter import filedialog
import cv2 as cv
from PIL import Image, ImageTk
from frames import Frames
from displayTumor import DisplayTumor
from predictTumor import *

class Gui:
    def __init__(self):
        self.MainWindow = tkinter.Tk()
        self.MainWindow.geometry('1200x720')
        self.MainWindow.resizable(width=False, height=False)
        self.MainWindow.title("Brain Tumor Detection")
        wWidth = 1180
        wHeight = 700
        self.DT = DisplayTumor()
        self.fileName = tkinter.StringVar()
        self.FirstFrame = Frames(self, self.MainWindow, wWidth, wHeight)
        self.FirstFrame.btnView['state'] = 'disabled'
        self.listOfWinFrame = [self.FirstFrame]
        WindowLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Brain Tumor Detection", height=1, width=40)
        WindowLabel.place(x=320, y=30)
        WindowLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"))
        self.val = tkinter.IntVar()
        RB1 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="Detect Tumor", variable=self.val, value=1, command=self.check)
        RB1.place(x=250, y=200)
        RB2 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="View Tumor Region", variable=self.val, value=2, command=self.check)
        RB2.place(x=250, y=250)
        browseBtn = tkinter.Button(self.FirstFrame.getFrames(), text="Browse", width=8, command=self.browseWindow)
        browseBtn.place(x=800, y=550)
        self.MainWindow.mainloop()

    def browseWindow(self):
        FILEOPENOPTIONS = dict(
            defaultextension='*.*',
            filetypes=[('jpg', '*.jpg'), ('png', '*.png'), ('jpeg', '*.jpeg'), ('All Files', '*.*')]
        )
        fileName = filedialog.askopenfilename(**FILEOPENOPTIONS)
        if not fileName:
            return
        pil_img = Image.open(fileName)
        cv_img = cv.imread(fileName)
        if cv_img is None:
            tkinter.messagebox.showerror("Error", "Failed to load image.")
            return
        pil_img = pil_img.convert('RGB')
        pil_img_np = np.array(pil_img)
        pil_img_np = pil_img_np[:, :, ::-1].copy()
        pil_img_np = Image.fromarray(pil_img_np)
        pil_img_np = pil_img_np.resize((250, 250), Image.Resampling.LANCZOS)
        pil_img_np = ImageTk.PhotoImage(pil_img_np)
        label = tkinter.Label(self.FirstFrame.getFrames(), image=pil_img_np)
        label.image = pil_img_np
        label.place(x=700, y=150)
        self.mriImage = cv_img
        self.DT.readImage(cv_img)

    def check(self):
        if not hasattr(self, 'mriImage'):
            tkinter.messagebox.showerror("Error", "Please browse and load an image first.")
            return
        choice = self.val.get()
        if choice == 1:
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
            self.listOfWinFrame = [self.FirstFrame]
            self.listOfWinFrame[0].setCallObject(self.DT)
            self.listOfWinFrame[0].setMethod(self.DT.removeNoise)
            secFrame = Frames(
                self,
                self.MainWindow,
                1180,
                700,
                function=self.DT.displayTumor,
                Object=self.DT
            )
            self.listOfWinFrame.append(secFrame)
            for i in range(len(self.listOfWinFrame)):
                if i != 0:
                    self.listOfWinFrame[i].hide()
            self.listOfWinFrame[0].unhide()
            if len(self.listOfWinFrame) > 1:
                self.listOfWinFrame[0].btnView['state'] = 'active'

mainObj = Gui()