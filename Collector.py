def collect(file):
    words = []
    file = open(file,"r").read()
    file +=" "
    lines = file.splitlines()
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
            else:
                word+=i
        
        words.append(line)
    return words