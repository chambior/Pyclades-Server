global FILENAME
FILE_NAME = "./assets/lang/FR_fr/FR_fr.help"

def read(file_name):
    file = open(file_name, encoding = 'utf-8')
    stream = file.read()
    help = {}
    cmd = ""
    desc = ""
    mode = "cmd"
    for char in stream:
        if char == '|':
            mode = "desc"
        elif char == '\n':
            help[cmd] = desc
            mode = "cmd"
            cmd = ""
            desc = ""
        else:
            if mode == "cmd":
                cmd += char
            elif mode == "desc":
                desc += char
    return help

def display(page = 1):
    i = 0
    help = read(FILE_NAME)
    print(help)
    res = "====== Help - Page {}/{} ======\n".format(page, int(len(help)/8)+1)
    for cmd in help:
        if (i >= ((page-1)<<3)) and ((i) < (page<<3)):
            res += ("{}. {}: {}\n".format(str(i+1), cmd, help[cmd]))
        i+=1
    return res
