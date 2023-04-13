def collect(file):
    words = []
    file = open(file,"r").read()
    file +=" "
    lines = file.splitlines()
    type = ""
    for t in lines:
        if not t.endswith(" "):
            t+=" "
        p = list(t)
        line = []
        word = ""
        for i in p:
            if i == " " or i == "\n":
                if word != "":
                    line.append(word)
                    word = ""
            elif i == "\"":
                if word != "":
                    line.append("\""+word+"\"")
                    word = ""
                    type = ""
                else:
                    type = "string"
            elif i == ".":
                if type == "":
                    line.append(word)
                    word = ""
            else:
                if i != "	":
                    word+=i
        if line != []:
            words.append(line)
    return words