# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import tkFileDialog
import os.path
import dealcsv
import ttk
import comparedata
import threading

ALLOWFILETYPES =[("CSV File","*.csv"),("Excel File","*.xls")]


class Application(Frame):
    def __init__(self,master):
        Frame.__init__(self,master,bd=1)
        self['width']=800
        
        self.lb_chooseFirstFile = Label(self,text="Choose File")
        self.lb_chooseSecondFile = Label(self,text="Choose File")
        self.lb_chooseFirstFile.grid(row=0,column=0,columnspan=2,sticky=W)
        self.lb_chooseSecondFile.grid(row=1,column=0,columnspan=2,sticky=W)        
        
        self.txt_firstfilename = Entry(self,width=30)
        self.txt_secondfilename = Entry(self,width=30)
        self.txt_firstfilename.grid(row=0,column=1,columnspan=2,sticky=W)
        self.txt_secondfilename.grid(row=1,column=1,columnspan=2,sticky=W)
        
        self.bt_openfirstfile = Button(self,text="OPEN FILE")
        self.bt_opensecondfile = Button(self,text="OPEN FILE")
        self.bt_openfirstfile.bind("<ButtonRelease-1>",self.selectFile)
        self.bt_opensecondfile.bind("<ButtonRelease-1>",self.selectFile)
        self.bt_openfirstfile.grid(row=0, column=2,columnspan=2,sticky=E)
        self.bt_opensecondfile.grid(row=1, column=2,columnspan=2, sticky=E)

        self.list_firstfilecolumns = Listbox(self,exportselection=False)
        self.list_secondfilecolumns = Listbox(self,exportselection=False)

        self.list_firstfilecolumns.grid( row=2,column=0,columnspan=3,sticky=W)
        self.list_secondfilecolumns.grid(row=2,column=1,columnspan=3,sticky=E)
        
        self.bt_addfirstincludecolumn = Button(self,text="添加需要导出的列")
        self.bt_addfirstincludecolumn.grid(row=3,column=0,columnspan=3,sticky=W)
        self.bt_addfirstincludecolumn.bind("<ButtonRelease-1>",self.addincludecolumn)

        self.bt_addsecondincludecolumn = Button(self,text="添加需要导出的列")
        self.bt_addsecondincludecolumn.grid(row=3,column=1,columnspan=3,sticky=E)
        self.bt_addsecondincludecolumn.bind("<ButtonRelease-1>",self.addincludecolumn)
    
        self.list_firstincludecolumns = Listbox(self,exportselection=False,selectmode=MULTIPLE)
        self.list_secondincludecolumns = Listbox(self,exportselection=False,selectmode=MULTIPLE)

        self.list_firstincludecolumns.grid( row=4,column=0,columnspan=3,sticky=W)
        self.list_secondincludecolumns.grid(row=4,column=1,columnspan=3,sticky=E)


        self.bt_delfirstincludecolumn = Button(self,text="删除需要导出的列")
        self.bt_delfirstincludecolumn.grid(row=5,column=0,columnspan=3,sticky=W)
        self.bt_delfirstincludecolumn.bind("<ButtonRelease-1>",self.delincludecolumn)

        self.bt_delsecondincludecolumn = Button(self,text="删除需要导出的列")
        self.bt_delsecondincludecolumn.grid(row=5,column=1,columnspan=3,sticky=E)
        self.bt_delsecondincludecolumn.bind("<ButtonRelease-1>",self.delincludecolumn)

        self.progressbar = ttk.Progressbar(self,length=300,mode="determinate")
        self.progressbar.grid(row=6,columnspan=6,sticky=W+S+N+E)

        self.ck_ratio = Checkbutton(self,text="相似比较")
        self.ck_ratio.grid(row=7,column=0,sticky=W)

        #self.lb_ratio_val = Label(self,text="最小相似度")
        #self.lb_ratio_val.grid(row=7,column=1,sticky=W)

        self.txt_ratio_val = Entry(self,width=10)
        self.txt_ratio_val.grid(row=7,column=1,sticky=W)

        self.bt_comparedata = Button(self,text="Start comparing data",fg="blue")
        self.bt_comparedata.grid(row=7,column=2,columnspan=4,sticky=W)
        self.bt_comparedata.bind("<ButtonRelease-1>",self.comparedata)
        
        self.msg_result = Message(self,text="msg result",fg="red",width=500)
        self.msg_result.grid(row=8,columnspan=6)

        print self.grid_size()
        self.pack()

        
    def delincludecolumn(self,event):      
        if event.widget ==self.bt_delfirstincludecolumn:
            self.delselecteditem(self.list_firstincludecolumns )
        elif event.widget ==self.bt_delsecondincludecolumn:
             self.delselecteditem(self.list_secondincludecolumns)

    def delselecteditem(self,sourcelist):
        selectedIndexes= sourcelist.curselection()
        print selectedIndexes
        if not selectedIndexes :
            return
        print selectedIndexes
        #将tuple转化为list
        selectedIndexes=list(selectedIndexes)
        #对索引排序，因为一次删除多个时，如果当前被删除项不是最后一项，ListBox中的索引会重新建立
        selectedIndexes.sort(lambda x,y:-1)       
        for index in selectedIndexes:
            sourcelist.delete(index)
           
    def addincludecolumn(self,event):      
        if event.widget ==self.bt_addfirstincludecolumn:
            self.addselecteditem(self.list_firstfilecolumns,self.list_firstincludecolumns)
        elif event.widget ==self.bt_addsecondincludecolumn:
             self.addselecteditem(self.list_secondfilecolumns,self.list_secondincludecolumns)

    def addselecteditem(self,sourcelist,targetlist):
        selectedIndexes= sourcelist.curselection()
        if not selectedIndexes :
            return
        selectedVal = sourcelist.get(selectedIndexes[0])
        #print selectedVal
        #check item exists
        values = targetlist.get(0,END)
        print values
        if selectedVal in values:
            return
        targetlist.insert(0,selectedVal)
        
    
    def selectFile(self,event):
        filename = tkFileDialog.askopenfilename(title="Please choose a file",filetypes=ALLOWFILETYPES)
        
        if event and event.widget == self.bt_openfirstfile:
            self.selectfirstfile(filename)
        elif event and event.widget == self.bt_opensecondfile:
            self.selectsecondfile(filename)

    def selectfirstfile(self,filename):
        self.txt_firstfilename.delete(0,END)
        self.list_firstfilecolumns.delete(0,END)
        self.list_firstincludecolumns.delete(0,END)

        self.txt_firstfilename.insert(0,filename)
        headercolumns = dealcsv.get_headers(filename)
        for item in headercolumns:
            self.list_firstfilecolumns.insert(0,item)
        
        #processbar = ttk.Progressbar(self,maximum=100,length=250)
        #self.processbar.pack()
        #processbar.start()

    def selectsecondfile(self,filename):
        self.txt_secondfilename.delete(0,END)
        self.list_secondfilecolumns.delete(0,END)
        self.list_secondincludecolumns.delete(0,END)
        self.txt_secondfilename.insert(0,filename)

        headercolumns = dealcsv.get_headers(filename)
        for item in headercolumns:
            self.list_secondfilecolumns.insert(0,item)
        


    def comparedata(self,event):
        #init thread argument
        self.progressbar['value']=0
        comparedata.hasproc_count = 0
        comparedata.totalcount=0

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
        print first_selected_columns
        print second_selected_columns
        #compare columns
        firstcolumns = self.list_firstfilecolumns.get(first_selected_columns[0])
        secondcolumns = self.list_secondfilecolumns.get(second_selected_columns[0])

        #include columns
        firstincludecolumns = self.list_firstincludecolumns.get(0,END)
        secondincludecolumns = self.list_secondincludecolumns.get(0,END)
        print firstincludecolumns
        print secondincludecolumns
        #print columns
        
        #result = comparedata.comparecsv(firstfile,secondfile,[firstcolumns],[secondcolumns],
        #                                list(firstincludecolumns),list(secondincludecolumns))
        comparethread = threading.Thread(target=self.startcomparedatathread,args=[firstfile,secondfile,firstcolumns,secondcolumns,
                                                      firstincludecolumns,secondincludecolumns]) 
        comparethread.start()
        import time
        time.sleep(2)
        thread = threading.Thread(target=self.startprogressbarthread)
        thread.start()



    def startcomparedatathread(self,firstfile,secondfile,firstcolumns,secondcolumns,firstincludecolumns,secondincludecolumns):
        import datetime
        print datetime.datetime.now()
        result = comparedata.comparecsv(firstfile,secondfile,[firstcolumns],[secondcolumns],
                                        list(firstincludecolumns),list(secondincludecolumns))

        if dealcsv.write_dict_to_csv(result,'result.csv'):
            self.msg_result["text"] = "文件生成成功，请查看当前目录下的result.csv文件"
            #tkMessageBox.showinfo(title="生成成功",message="文件生成成功，请查看当前目录下的result.csv文件")
        else:
            self.msg_result["text"] = "文件生成失败"
            #tkMessageBox.showerror(title="生成失败",message="没有匹配的记录")
        print datetime.datetime.now()

    def startprogressbarthread(self):
        print "thread.totalcount=%s,thread.hasproc_count=%s"%(comparedata.totalcount,comparedata.hasproc_count)
        complete_percent =10 # int(float(comparedata.hasproc_count)/comparedata.totalcount*100)
        #print "complete_percent=%s"%complete_percent
        #while comparedata.hasproc_count<comparedata.totalcount:
        while complete_percent<100:
            complete_percent = int(float(comparedata.hasproc_count)/comparedata.totalcount*100)
            print "complete_percent=%s"%complete_percent
            self.msg_result["text"] = "当前任务的处理进度%s%%" % complete_percent
            #self.progressbar.step(complete_percent)
            self.progressbar["value"] = complete_percent
            if complete_percent<100:
                import time
                time.sleep(1)
            else:
                self.msg_result["text"] = "文件生成成功，请查看当前目录下的result.csv文件"


if __name__ == "__main__":
    master = Tk()
    app = Application(master)
    app.mainloop()
