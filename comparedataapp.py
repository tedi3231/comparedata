# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import tkFileDialog
import os.path
import dealcsv
import ttk
import comparedata

ALLOWFILETYPES =[("CSV File","*.csv"),("Excel File","*.xls")]

class Application(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        
        self.lb_chooseFirstFile = Label(self,text="Choose File")
        self.lb_chooseSecondFile = Label(self,text="Choose File")
        
        self.txt_firstfilename = Entry(self,width=50)
        self.txt_secondfilename = Entry(self,width=50)
        
        self.bt_openfirstfile = Button(self,text="OPEN FILE")
        self.bt_opensecondfile = Button(self,text="OPEN FILE")
        
        self.bt_openfirstfile.bind("<Button-1>",self.selectFile)
        self.bt_opensecondfile.bind("<Button-1>",self.selectFile)
        
        self.lb_chooseFirstFile.grid(row=0,sticky=W)
        self.lb_chooseSecondFile.grid(row=1,sticky=W)

        self.txt_firstfilename.grid(row=0,column=1)
        self.txt_secondfilename.grid(row=1,column=1)

        self.bt_openfirstfile.grid(row=0,column=2,columnspan=2)
        self.bt_opensecondfile.grid(row=1,column=2,columnspan=2)

        self.list_firstfilecolumns = Listbox(self,width=30,exportselection=False)
        self.list_secondfilecolumns = Listbox(self,width=30,exportselection=False)

        self.list_firstfilecolumns.grid(row=2,columnspan=2,sticky=W)
        self.list_secondfilecolumns.grid(row=2,columnspan=2,sticky=E)
        

        self.bt_comparedata = Button(self,text="Start comparing data")
        self.bt_comparedata.grid(row=3,columnspan=3,sticky=W)
        self.bt_comparedata.bind("<Button-1>",self.comparedata)

        self.pack()

    def selectFile(self,event):
        filename = tkFileDialog.askopenfilename(title="Please choose a file",filetypes=ALLOWFILETYPES)
        
        if event and event.widget == self.bt_openfirstfile:
            self.selectfirstfile(filename)
        elif event and event.widget == self.bt_opensecondfile:
            self.selectsecondfile(filename)

    def selectfirstfile(self,filename):
        self.txt_firstfilename.delete(0,END)
        self.txt_firstfilename.insert(0,filename)
        headercolumns = dealcsv.get_headers(filename)
        for item in headercolumns:
            self.list_firstfilecolumns.insert(0,item)

        #processbar = ttk.Progressbar(self,maximum=100,length=250)
        #self.processbar.pack()
        #processbar.start()

    def selectsecondfile(self,filename):
        self.txt_secondfilename.delete(0,END)
        self.txt_secondfilename.insert(0,filename)

        headercolumns = dealcsv.get_headers(filename)
        for item in headercolumns:
            self.list_secondfilecolumns.insert(0,item)

    def comparedata(self,event):
        firstfile = self.txt_firstfilename.get()
        secondfile = self.txt_secondfilename.get()

        #print 'firstfile=%s,secondfile=%s'%(firstfile,secondfile)
        
        if firstfile.strip()=='':
            tkMessageBox.showerror(title="Error",message="First file can't be empty")
            return

        if secondfile.strip()=='':
            tkMessageBox.showerror(title="Error",message="Second file can't be empty")
            return
        
        #firstdatas = dealcsv.get_content_with_directory(firstfile)
        #seconddatas = dealcsv.get_content_with_directory(secondfile)

        first_selected_columns = self.list_firstfilecolumns.curselection()
        second_selected_columns = self.list_secondfilecolumns.curselection()

        if not first_selected_columns:
            tkMessageBox.showerror(title="Error",message="First file no column selected")
            return

        if not second_selected_columns:
            tkMessageBox.showerror(title="Error",message="Second file no column selected")
            return

        columns = self.list_firstfilecolumns.get(first_selected_columns[0])
        #print columns
        import datetime
        print datetime.datetime.now()
        result = comparedata.comparecsv(firstfile,secondfile,[columns])
        print datetime.datetime.now()
        print len(result)

if __name__ == "__main__":
    master = Tk()
    app = Application(master)
    app.mainloop()
