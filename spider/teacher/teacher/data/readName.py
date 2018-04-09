
def readXin(fileName):
    xin=[]
    f=open(fileName)
    while 1:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        if len(line)>1:

            names=line.split(' ')
            for n in names:
                xin.append(n)
    return xin