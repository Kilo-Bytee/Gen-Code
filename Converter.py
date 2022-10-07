import Collector

class run():
    def __init__(self,file):
        if not file.endswith(".gen"):
            print("Error: Incorrect file type")
            exit()

        keywords = Collector.collect(file)

        run.Clear_Var()
        Define_Functions(keywords)

        type = None

        for line in keywords:
            ignore = False
            for i in line:
                if i == "":
                    line.remove(i)
                
                if i.startswith("---"):
                    ignore = True

                if ignore == False:
                    if i == "print":
                        type = "PRINT"
                    elif i == "var":
                        type = "VARIABLE"

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

            elif type == "FUNCTION":
                pass

    def Print(args,type):
        sign = ""
        result = None
        args.remove("print")
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

    def Clear_Var():
        file = open("vars.txt","w")
        file.close()

class Define_Functions():
    def __init__(self,Lines):
        for line in Lines:
            print(line)
            try:
                if line[0] == "func":
                    print("Function detected",line[1])
            except:
                pass

run("Test.gen")