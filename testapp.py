# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import tkFileDialog
import os.path
import ttk

class Application(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.bt_openfirstfile = Button(self,text="Add Button")
        self.bt_openfirstfile.bind("<Button-1>",self.addbutton)
        self.bt_openfirstfile.grid(row=0,column=1,sticky=W)
        
        self.bottomcontainer = Frame(self,bg='red')
        self.bottomcontainer.grid(row=1,column=0,columnspan=2,sticky=W)
        self.bottomcontainer.pack()
        
        self.pack()

    def addbutton(self,event):        
        size = self.grid_size()
        print size
        self.grid_propagate(True)
        Button(self,text="New Button").grid(row=size[0]+1,column=1)

if __name__ == "__main__":
    master = Tk()
    app = Application(master)
    app.mainloop()
        
