# -*- coding: utf-8 -*-
import Tkinter
from Tkinter import *
import tkMessageBox
import tkFileDialog
import os.path
import ttk
import time
import threading

class Application(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.pb1 = ttk.Progressbar(self,length=100,mode="determinate",name="pb1")
        pb2 = ttk.Progressbar(self,mode="indeterminate",name="pb2")
        #start = ttk.Button(text="Start",command = lambda:self._do_start())
        self.bt_start=ttk.Button(self,text="start",command=lambda:self._do_start()) 
        self.pb1.grid(row=0,column=0)
        self.bt_start.grid(row=1,column=0)
        
        self.pack()
    
    def start_thread(self):
        #count = 100
        
        for i in range(10,100,10):
            self.pb1.step(10)
            time.sleep(1)
        
        print "start_thread"
        #self.pb1.step(50)
        print 'abc'

    def _do_start(self):
        thread = threading.Thread(target=self.start_thread)
        thread.start()
        #thread.join()
        self.pb1.step(10)
        for i in range(10):
            pass
            #self.pb1.start()
            #self.pb1.step(10)
            #time.sleep(2)
            #self.pb1.stop()

if __name__ == "__main__":
    master = Tk()
    app = Application(master)
    app.mainloop()
        
