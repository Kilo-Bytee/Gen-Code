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

        if file != None:
            run.file = file
        
        self.mainmenu.add_cascade(menu=self.filemenu,label="File")

        self.mainmenu.add_command(label="Run",command=self.run_file)

        self.filemenu.add_command(label="New File",command=run)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Open File",command=self.open_file)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Save As",command=lambda:self.save_file("SA"))
        self.filemenu.add_command(label="Save",command=lambda:self.save_file("S"))

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
        else:
            if self.file != None:      
                e = open(self.file,"w")
                e.write(content)
                e.close()
    
    def open_file(self):
        place = filedialog.askopenfilename()
        if place != '':
            content = open(place,"r").read()
            self.file = place
            self.text.delete("1.0",END)
            self.text.insert("1.0",content)

run()