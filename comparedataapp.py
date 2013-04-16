from Tkinter import *
import tkMessageBox
import tkFileDialog
import os.path

ALLOWFILETYPES =[("PDF File","*.pdf"), ("Excel File","*.xls"), ("Word File","*.docx"),("Python File","*.py")]

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

        self.list_firstfilecolumns = Listbox(self,width=30)
        self.list_secondfilecolumns = Listbox(self,width=30)

        self.list_firstfilecolumns.grid(row=2,columnspan=2,sticky=W)
        self.list_secondfilecolumns.grid(row=2,columnspan=2,sticky=E)
        self.pack()

    def selectFile(self,event):
        #print event.widget == self.bt_opensecondfile
        #print dir(event.widget)
        filename = tkFileDialog.askopenfilename(title="Please choose a file",filetypes=ALLOWFILETYPES)
        if( os.path.getsize(filename)<=100 ):
            tkMessageBox.showwarning(title="Wanring",message="The selected file can't be empty")
        
        if event and event.widget == self.bt_openfirstfile:
            self.selectfirstfile(filename)
        elif event and event.widget == self.bt_opensecondfile:
            self.selectsecondfile(filename)

    def selectfirstfile(self,filename):
        self.txt_firstfilename.delete(0,END)
        self.txt_firstfilename.insert(0,filename)

    def selectsecondfile(self,filename):
        self.txt_secondfilename.delete(0,END)
        self.txt_secondfilename.insert(0,filename)

if __name__ == "__main__":
    master = Tk()
    app = Application(master)
    app.mainloop()
