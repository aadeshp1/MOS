import os

M = [['\0' for i in range(4)] for j in range(100)]
buffer = ['\0' for i in range(40)]
IR = [0 for i in range(4)]
IC = [0 for i in range(2)]
R = [0 for i in range(4)]
C = False
SI = 0 


def INIT():
    global M,IR,IC,R,C,SI,buffer
    M = [['\0' for i in range(4)] for j in range(100)]
    IR = [0 for i in range(4)]
    IC = 0
    R = [0 for i in range(4)]
    C = False
    SI = 0 
    buffer = ['\0' for i in range(40)]
    LOAD()


def main():
    if os.path.exists("ipp1.txt"):
        print("File Exists")
        global fi,fo
        fi=open("ipp1.txt","r")
        fo=open("opp1.txt","w")   
    else:
        print("File Does Not Exist")
    INIT()

def EXECUTEUSERPROGRAM():
    global IC,IR,R,M,C,SI
    print("M=",M)
    while(True):
        print("IR=",IR)
        IR=M[IC]
        IC=IC+1
        if(IR[0]=='L' and IR[1]=='R'):
            R=M[int(IR[2])*10 + int(IR[3])]
        elif(IR[0]=='S' and IR[1]=='R'):
            M[int(IR[2])*10 + int(IR[3])]=R
        elif(IR[0]=='C' and IR[1]=='R'):
            if(M[int(IR[2])*10 + int(IR[3])]==R):
                C=True
            else:
                C=False
        elif(IR[0]=='B' and IR[1]=='T'):
            if(C):
                IC=int(IR[2])*10 + int(IR[3])
        elif(IR[0]=='G' and IR[1]=='D'):
            SI=1
            MOS()
        elif(IR[0]=='P' and IR[1]=='D'):
            SI=2
            MOS()
        elif(IR[0]=='H'):
            SI=3
            MOS()
            break

def READ():
    i=0
    j=0
    global IR,buffer,M
    buffer=fi.readline()
    n = int(IR[2])*10
    while(buffer[i]!='\n'):
        M[n][j] = buffer[i]
        if(j==3):
            j=0
            n+=1
        else:
            j+=1
        i += 1
    # M[n][j] = '\n'

def WRITE():
    global IR,M,fo
    n = int(IR[2])*10
    for i in range(n, n + 10):
        for j in range(4):
            if (M[i][j] == '\0'):
                break
            print(M[i][j], end="", file=fo)
    print('', file=fo)
    i=0

def TERMINATE():
    for i in range(100):
        print(i, end=" ")
        print(M[i])
    print('', file=fo)
    print('', file=fo)
    print("Job Terminated")
    INIT()

def START_EXECUTION():
    IC=0
    EXECUTEUSERPROGRAM()

def MOS():
    if(SI==1):
        READ()
    elif(SI==2):
        WRITE()
    elif(SI==3):
        TERMINATE()

def LOAD():
    print("Fetching...")
    global buffer
    a=True
    m=0
    while(a):
        buffer = fi.readline()
        if not buffer:
            a=False
            continue
        if(buffer[0]=='$'):
            if(buffer[1:4]=='AMJ'):
                print("Reading...")
                global id, time, lines_printed
                id = buffer[4:8]
                time = buffer[8:12]
                lines_printed = buffer[12:16]
            elif(buffer[1:4]=='DTA'):
                print("Reading Data...")
                START_EXECUTION()
            elif(buffer[1:4]=='END'):
                INIT()
        else:
            if(m==100):
                print("Abort! Memory Exceeded")
                exit(-1)
            else:
                i = 0
                for k in range(m,m+10):
                    if (buffer[i] == 'H'):
                        M[k][0] = buffer[i]
                        M[k][1] = '\x00'
                        M[k][2] = '\x00'
                        M[k][3] = '\x00'
                        i += 4
                        break
                    else:
                        if buffer[i]=='\n' or buffer[i+1]=='\n' or buffer[i+2]=='\n' or buffer[i+3]=='\n':
                            break
                        else:
                            M[k][0:4] = buffer[i:i + 4]
                            i += 4
                m=m+10
        


main()