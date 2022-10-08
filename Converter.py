import Collector
import json as js

class run():
    ful_ignore = False
    def __init__(self,file,typ="file"):
        keywords = None
        if typ == "file":
            if not file.endswith(".gen"):
                print("Error: Incorrect file type")
                exit()
            else:
                keywords = Collector.collect(file)
                Define_Functions(keywords)

        elif typ == "func":
            keywords = file

        Func_Names = Define_Functions.Get_Names()
        type = None
        for line in keywords:

            for i in line:
                
                if i == "":
                    line.remove(i)
                
                if i.startswith("---"):
                    run.ful_ignore = True
                elif i == "func":
                    run.ful_ignore = True
                elif i == "end":
                    run.ful_ignore = False

                if run.ful_ignore == False:
                    if i == "print":
                        type = "PRINT"
                    elif i == "var":
                        type = "VARIABLE"
                    elif i in Func_Names:
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
                    result = run.Get_Var(args[0])
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
        variable = "\""
        for i in range(len(args)):
            if i > 2: 
                args[i] = run.Remove_Marks(args[i])
                variable+=args[i]+" "

        if variable.endswith(" "):
            variable = variable[:-1]
        file.write(args[1]+" "+variable+"\"\n")
        file.close()

    def Get_Var(var):
        file = open("vars.txt","r").read()
        vars = file.splitlines()
        result = ""
        found = False
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
        if found == False:
            print("Error: No variable named: "+var[0])

        return result

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