from fileinput import isfirstline
import Collector
import json as js

class run():
    Func_Names = None
    ful_ignore = False
    file = []
    def __init__(self,file,typ="file"):
        keywords = None
        if typ == "file":
            if not file.endswith(".gen"):
                print("Error: Incorrect file type")
                exit()
            else:
                keywords = Collector.collect(file)
                Define_Functions(keywords)
                run.file = keywords

        elif typ == "func":
            keywords = file

        run.Func_Names = Define_Functions.Get_Names()
        type = None
        for line in keywords:

            for i in line:
                
                if i == "":
                    line.remove(i)
                
                if i.startswith("---"):
                    type = "COMMENT"
                elif i == "func":
                    run.ful_ignore = True
                elif i == "end":
                    run.ful_ignore = False
                elif i == "endif":
                    run.ful_ignore = False

                if run.ful_ignore == False:
                    if i == "print":
                        type = "PRINT"
                    elif i == "var":
                        type = "VARIABLE"
                    elif i == "if":
                        type = "IF"

                    elif i in run.Func_Names:
                        Func = Define_Functions.Get_Func(i)
                        run(Func,"func")

            if run.ful_ignore == False:
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
                elif type == "COMMENT":
                    pass
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
        file = open("vars.txt","a")
        variable = ""
        typ = ""
        print("Var",args)
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
        file = open("vars.txt","r").read()
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
            print(var)
            print("Error: No variable named: "+var)

        return result, typ

    def Remove_Marks(i):
        if i.startswith("\""):
            i = i[1:]

        if i.endswith("\""):
            i = i[:-1]
        return i 

    def Clear():
        file = open("vars.txt","w")
        file.close()
        file = open("functions.json","w")
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
        print(args)
        if not args[1].startswith("\"") and not args[1].isdigit() and not args[1] == "TRUE" or not args[1] == "FALSE":
            if args[1] != "TRUE" and args[1] != "FALSE":
                args[1],typ = run.Get_Var(args[1])

        if not args[3].startswith("\"") and not args[3].isdigit():
            if args[3] != "TRUE" and args[3] != "FALSE":
                args[3],typ = run.Get_Var(args[3])

        Ans = True
        i = 1
        while(i < len(args)):
            if args[i+1] == "=":
                if not args[i] == args[i+2]:
                    Ans = False
                    print(args)

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
        for line in Lines:
            try:
                if function == True:
                    func_lines.append(line)
                    
                if line[0] == "func":
                    Name = line[1]
                    function = True
                elif line[0] == "end":
                    function = False
                    Define_Functions.Save(func_lines,Name)
                    Name = ""
                    func_lines = []
            except:
                pass

    def Save(args,Name):
        red = open("functions.json","r").read()
        red = js.loads(red)

        content = open("functions.json","w")

        content_text = [Name,args]
        red.append(content_text)
        
        content.write(js.dumps(red))
        content.close()

    def Get_Names():
        content = open("functions.json","r").read()
        content = js.loads(content)
        Names = []
        for i in content:
            Names.append(i[0])

        return Names

    def Get_Func(Name):
        content = open("functions.json","r").read()
        content = js.loads(content)
        for i in content:
            if i[0] == Name:
                return i[1]

run.Clear()
run("Test.gen")