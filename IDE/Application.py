from tkinter import *
from tkinter import filedialog
import os
import sys

dirname = os.path.dirname(__file__).split("\IDE")
dirname = dirname[0]

sys.path.insert(0,dirname)

import GenConverter.Converter as converter

class run():
    file = None
    def __init__(self,file=None):
        self.app = Tk()
        self.app.title("Generation")
        self.app.geometry("600x700")

        self.mainmenu = Menu()
        self.filemenu = Menu(tearoff=0)
        self.recent = Menu(tearoff=0)

        if file != None:
            run.file = file
        
        self.mainmenu.add_cascade(menu=self.filemenu,label="File")

        self.mainmenu.add_command(label="Run",command=self.run_file)

        self.filemenu.add_command(label="New File",command=run)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Open File",command=self.open_file)
        self.filemenu.add_cascade(menu=self.recent,label="Open Recent")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Save As",command=lambda:self.save_file("SA"))
        self.filemenu.add_command(label="Save",command=lambda:self.save_file("S"))

        file = open(dirname+r"\IDE\History.txt").read().splitlines()
        for i in file:
            split = i.split(" ")
            self.recent.add_command(label=split[0],command=lambda:self.open_recent(split[1]))

        self.app.config(menu=self.mainmenu)

        self.text = Text(self.app,font="Arial 10")
        self.text.place(relheight=1,relwidth=1)

        self.app.mainloop()
    
    def run_file(self):
        content = self.text.get("1.0",END)
        if self.file != None:
            file = open(self.file,"r").read()
            if file == content:
                converter.run(self.file)
            else:
                self.save_file("S")
                converter.run(self.file)
        else:
            self.save_file("SA")
            converter.run(self.file)
    
    def save_file(self,type):
        content = self.text.get("1.0",END)
        if type == "SA":
            place = filedialog.asksaveasfilename()
            if place != "":
                self.file = place+".gen"
                e = open(place+".gen","w")
                e.write(content)
                e.close()
                self.save_recent()
            else:
                pass
        else:
            if self.file != None:      
                e = open(self.file,"w")
                e.write(content)
                e.close()
                self.save_recent()
            else:
                pass
    
    def open_file(self):
        place = filedialog.askopenfilename()
        if place != '':
            content = open(place,"r").read()
            self.file = place
            self.text.delete("1.0",END)
            self.text.insert("1.0",content)

    def open_recent(self,place):
        content = open(place,"r").read()
        self.file = place
        self.text.delete("1.0",END)
        self.text.insert("1.0",content)

    def save_recent(self):
        file = open(dirname+r"\IDE\History.txt","r").read().splitlines()
        line = ""
        split = self.file.split("/")
        line+=split[(len(split)-1)]+" "+self.file
        t = False
        new = ""

        if not line in file:
            if len(file) == 5:
                new += line+"\n"
                for i in range(0,4):
                    new+=file[i]+"\n"
            else:
                if len(file) != 0:
                    new += line+"\n"
                    for i in range(len(file)):
                        new+=file[i]+"\n"
                else:
                    new += line+"\n"
        else:
            if len(file) == 1:
                new += line+"\n"
        file = open(dirname+r"\IDE\History.txt","w")
        file.write(new)
        file.close()

run()