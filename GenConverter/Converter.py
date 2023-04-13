import os
import sys
import importlib
import importlib.util

dirname = os.path.dirname(__file__).split("\GenConverter")
dirname = dirname[0]

sys.path.insert(1,dirname)

import GenConverter.Collector as Collector
import json as js

class run():
    Func_Names = []
    ful_ignore = False
    file = []
    def __init__(self,file,typ="file"):
        keywords = None
        if typ == "file":
            run.Clear()
            if not file.endswith(".gen"):
                print("Error: Incorrect file type")
                exit()
            else:
                keywords = Collector.collect(file)
                Define_Functions(keywords)
                run.file = keywords

        elif typ == "func":
            keywords = file
        
        try:
            run.Func_Names = Define_Functions.Get_Names()
        except:
            pass
        type = None
        for line in keywords:
            for i in line:
                ignore = False
                if i == "":
                    line.remove(i)
                
                if i.startswith("##"):
                    ignore = True
                elif i == "func":
                    run.ful_ignore = True
                elif i == "end":
                    run.ful_ignore = False
                elif i == "endif":
                    run.ful_ignore = False

                if run.ful_ignore == False and ignore == False:
                    if i == "print":
                        type = "PRINT"
                    elif i == "var":
                        type = "VARIABLE"
                    elif i == "if":
                        type = "IF"
                    elif i == "use":
                        type = "IMPORT"
            p = line[0]
            func_test = p[:-2]
            try:
                if line[0] in run.Func_Names.keys():
                    Func = Define_Functions.Get_Func(line[0],line[1])
                    run(Func,"func")
                elif func_test in run.Func_Names["Global"]:
                    Func = Define_Functions.Get_Func(func_test)
                    run(Func,"func")
            except:
                pass

            if run.ful_ignore == False and ignore == False:
                if type == "PRINT":
                    if i.startswith("\""):
                        run.Print(line,"str")
                        type = None
                    elif i.isdigit():
                        run.Print(line,"num")
                        type = None
                    else:
                        run.Print(line,"var")
                        type = None

                elif type == "VARIABLE":
                    run.Create_Var(line)
                    type = None

                elif type == "IF":
                    If_Statement(line)
                    run.ful_ignore = True
                    type = None

                elif type == "IMPORT":
                    Import(line)
                    type = None
            else:
                type = None

    def Print(args,type):
        sign = ""
        result = None
        args.remove("print")
        if run.ful_ignore == False:
            if type == "num":
                for i in args:
                    if i == "+" or i == "-" or i == "/" or i =="*":
                        sign = i
                    try:
                        num = int(i)
                        if sign == "":
                            result = num
                        else:
                            if sign == "+":
                                result += num
                            elif sign == "-":
                                result -= num
                            elif sign == "*":
                                result *= num
                            elif sign == "/":
                                result /= num
                    except:
                        print("error")
            elif type == "var":
                try:
                    result,typ = run.Get_Var(args[0])
                except:
                    pass

            if type == "num" or type == "var":
                if result != None:
                    print(result)
            elif type == "str":
                string = ''
                for i in args:
                    if i.startswith("\""):
                        i = i[1:]
                    if i.endswith("\""):
                        i = i[:-1]

                    string += (i+" ")
                print(string)

    def Create_Var(args):
        file = open(dirname+r"\GenConverter\Value\vars.txt","a")
        variable = ""
        typ = ""
        if args[len(args)-1].startswith("\""):
            typ = "str"
        elif not args[3].startswith("\"") and args[3].isdigit():
            typ = "num"
        elif not args[3].startswith("\"") and args[3] == "TRUE" or not args[3].startswith("\"") and args[3] == "FALSE":
            typ = "sta"

        for i in range(len(args)):
            if i > 2: 
                args[i] = run.Remove_Marks(args[i])
                variable+=args[i]+" "

        if variable.endswith(" "):
            variable = variable[:-1]
        file.write(args[1]+" "+variable+" "+typ+"\n")
        file.close()

    def Get_Var(var):
        file = open(dirname+r"\GenConverter\Value\vars.txt","r").read()
        vars = file.splitlines()
        result = ""
        typ = ""
        found = False
        if var == "TRUE" or var == "FALSE":
            return
        for i in vars:
            q = i.split(" ")
            if q[0] == var:
                found = True
                st = ""
                for t in i:
                    if t != q[0]:
                        st += t
                if st.startswith(q[0]):
                    st = st[len(q[0])+1:]
                result = run.Remove_Marks(st)
                typ = q[2]
        result = result[:-4]
        if found == False:
            print("Error: No variable named: "+var)

        return result, typ

    def Remove_Marks(i):
        if i.startswith("\""):
            i = i[1:]

        if i.endswith("\""):
            i = i[:-1]
        return i 

    def Clear():
        file = open(dirname+r"\GenConverter\Value\vars.txt","w")
        file.close()
        file = open(dirname+r"\GenConverter\Value\functions.json","w")
        file.write("[]")
        file.close()

class If_Statement():
    def __init__(self, args):
        Answer = If_Statement.Question(args)
        If_Statement.Responce(Answer,args)

    def Responce(answer,line):
        Code = run.file
        collect = False
        At_Point = False
        Lines = []

        for i in Code:
            if collect == True:
                Lines.append(i)
                
            try:   
                if i == line:
                    At_Point= True
                    if answer == True:
                        collect = True

                if i[0] == "else":
                    if answer == False and At_Point == True:
                        collect = True
                    else:
                        collect = False

                elif i[0] == "endif":
                    collect = False
            except:
                pass

        run.ful_ignore = False

        run(Lines,"func")

    def Question(args):
        Ans = True
        i = 1
        while(i < len(args)):
            if not args[i].startswith("\"") and not args[i].isdigit():
                if args[i] != "TRUE" and args[i] != "FALSE":
                    args[i],typ = run.Get_Var(args[i])
                    if typ == "str":
                        args[i] = "\""+args[i]+"\""

            if not args[i+2].startswith("\"") and not args[i+2].isdigit():
                if args[i+2] != "TRUE" and args[i+2] != "FALSE":
                    args[i+2],typ = run.Get_Var(args[i+2])
                    if typ == "str":
                        args[i+2] = "\""+args[i+2]+"\""

            if args[i+1] == "=":
                if not args[i] == args[i+2]:
                    Ans = False

            if args[i+1] == "!=":
                if not args[i] != args[i+2]:
                    Ans = False

            elif args[i+1] == ">":
                if args[i].isdigit() and args[i+2].isdigit:
                    if not args[i] > args[i+2]:
                        Ans = False

            elif args[i+1] == "<":
                if args[i].isdigit() and args[i+2].isdigit:
                    if not args[i] < args[i+2]:
                        Ans = False

            elif args[i+1] == ">=":
                if args[i].isdigit() and args[i+2].isdigit:
                    if not args[i] >= args[i+2]:
                        Ans = False

            elif args[i+1] == "<=":
                if args[i].isdigit() and args[i+2].isdigit:
                    if not args[i] <= args[i+2]:
                        Ans = False
            i += 4

        return Ans
            
class Define_Functions():
    def __init__(self,Lines):
        function = False
        func_lines = []
        Name = ""
        Module = None
        for line in Lines:
            try:
                if function == True:
                    func_lines.append(line)
                    
                if line[0] == "func":
                    Name = line[1]
                    nam = ""
                    e = False
                    if not Name.endswith(")"):
                        print("Function:",Name,"Is inputed wrong")
                    else:
                        function = True

                    for i in Name:
                        if e == False:
                            if i != "(":
                                nam+=i
                            else:
                                e = True
                                Name = nam
                elif line[0] == "end":
                    if function == True:
                        function = False
                        Define_Functions.Save(func_lines,Name,Module)
                        Name = ""
                        func_lines = []
                elif line[0] == "Module":
                    Module = line[1][:-1]
                elif line[0] == "]":
                    Module = None
            except:
                pass

    def Save(args,Name,Module):

        red = open(dirname+r"\GenConverter\Value\functions.json","r").read()
        red = js.loads(red)
        
        content_text = [Name,args]

        
        if red == []:
            red.append({"Global":[]})

        f = False
        for i in red[0].keys():
            if i == Module:
                t = red[0]
                t[i].append(content_text)
                f = True

        if f == False and Module == None:
            t = red[0]
            t["Global"].append(content_text)
            
        elif f == False and Module != None:
            t = red[0]
            t.update({Module:[]})
            
            Mod = t[Module]
            Mod.append(content_text)
        
        content = open(dirname+r"\GenConverter\Value\functions.json","w")
        content.write(js.dumps(red))
        content.close()

    def Get_Names():
        content = open(dirname+r"\GenConverter\Value\functions.json","r").read()
        content = js.loads(content)
        content = content[0]
        Names = {}
        for i,v in content.items():
            current = []
            for func in v:
                current.append(func[0])
            
            Names.update({i:current})

        return Names

    def Get_Func(Module,Name=None):
        content = open(dirname+r"\GenConverter\Value\functions.json","r").read()
        content = js.loads(content)
        func = None
        if Name == None:
            t = content[0]
            for i in t["Global"]:
                if i[0] == Module:
                    func = i[1]
        else:
            t = content[0]
            Name = Name[:-2]
            for i in t[Module]:
                if i[0] == Name:
                    func = i[1]
        
        return func

class Import():
    def __init__(self,line):
        Name = line[1]+".py"
        
        files = os.listdir(dirname+r"\GenConverter\Modules")

        if Name in files:
            Loc = dirname+r"\GenConverter\Modules"
            Spec = importlib.util.spec_from_file_location(Loc,Loc+"\\"+Name)
            Module = Spec.loader.load_module()
        else:
            raise TypeError("No module called: "+line[1])