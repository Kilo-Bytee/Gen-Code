from tkinter import *
import os
import sys

dirname = os.path.dirname(__file__).split("\GenConverter")
dirname = dirname[0]

sys.path.insert(1,dirname)

class suggets():
    def __init__(self, word):
        suggetions = self.get_suggestions(word)

        Listbox()


    def get_suggestions(self,word):
        if word == "if":
            return Functions.Get_Vars()

class Functions:
    def Get_Vars():
        file = open(dirname+r"\GenConverter\Value\vars.txt","r").read()
        vars = file.splitlines()
        tab = []
        for i in vars:
            split = i.split(" ")
            tab.append(split[0])

        return tab