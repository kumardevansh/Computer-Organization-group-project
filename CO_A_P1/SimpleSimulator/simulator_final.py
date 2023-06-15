X=[]
Y=[]

def convert1(a):
    # convert integer to 16 bit binary
    bnr = bin(a)[2:]
    # this reverses an array
    x=''
    klen=len(bnr)-1
    while klen>=0:
        x+=bnr[klen]
        klen-=1
    # this adds 0
    for bis in range(16-len(x)):
        x += '0'
    # this reverses an array
    bnr=''
    klen=len(x)-1
    while klen>=0:
        bnr+=x[klen]
        klen-=1
    return bnr



def convert(a):
    # convert integer to 8 bit binary
    bnr = bin(a)[2:]
    # this reverses an array
    x=''
    klen=len(bnr)-1
    while klen>=0:
        x+=bnr[klen]
        klen-=1
    for bis in range(7- len(x)):
        x += '0'
    # this reverses an array
    bnr=''
    klen=len(x)-1
    while klen>=0:
        bnr+=x[klen]
        klen-=1
    return bnr

statements = {}
var = 0
pc ="0000000"
reg = {'000': "0000000000000000",
       '001': "0000000000000000",
       '010': "0000000000000000",
       '011': "0000000000000000",
       '100': "0000000000000000",
       '101': "0000000000000000",
       '110': "0000000000000000",
       '111': "0000000000000000"}
while (1):
    try:
        line = input()
        if(line!=""):
            statements[convert(var)] = line
            var += 1
    except EOFError:
        break
# print(statements)
MEM = statements.copy()
mlen = len(MEM)
while (mlen <= 127):#changed 255 to 127
    MEM[convert(mlen)] = "0000000000000000"
    mlen+=1
def mov1(l,pc):
    # regmov=[]
    # regmov.append("0000000000000000")
    reg["111"]="0000000000000000"
    # regmov[1]=convert1(regmov[0])
    reg[l[6:9]]=convert1(int(l[9:], 2))
    return convert(int(pc,2)+1)

def f_mov1(l,pc):
    reg["111"]="0000000000000000"
    reg[l[5:8]]=convert1(int(l[8:], 2))
    return convert(int(pc,2)+1)


def mov2(l,pc):
    reg[l[10:13]]=convert1(int(reg[l[13:]],2))
    reg["111"]="0000000000000000"
    return convert(int(pc,2)+1)


def add(l,pc):
    reg["111"] = "0000000000000000"
    n1 = int(reg[l[10:13]], 2)
    n2 = int(reg[l[13:16]], 2)
    x = (n1 + n2)
    y = bin(x)
    if len(y) > 18:
        reg[l[7:10]] = y[-16:]
        reg['111'] = convert1(int(reg['111'], 2) + 8)
    else:
        reg[l[7:10]] = convert1(x)
    return convert(int(pc, 2) + 1)


def f_add(l, pc):
    reg["111"] = "0000000000000000"
    n1 = int(reg[l[10:13]], 2)  # Extracting register 1 value
    n2 = int(reg[l[13:16]], 2)  # Extracting register 2 value
    x = n1 + n2

    # Handling overflow
    if x >= 256:
        overflow_flag = True
        reg[l[7:10]] = '00000000'  # Setting register 1 to 0
    else:
        overflow_flag = False
        reg[l[7:10]] = bin(x)[2:].zfill(8)  # Updating register 1 with the result

    return convert(int(pc, 2) + 1)

def sub(l,pc):
    reg["111"] = "0000000000000000"
    n1 = int(reg[l[10:13]], 2)
    n2 = int(reg[l[13:16]], 2)
    x = (n1 - n2)
    if x < 0:
        reg[l[7:10]] ="0000000000000000"
        reg['111'] = convert1(int(reg['111'], 2) + 8)
    else:
        reg[l[7:10]] = convert1(x)
    return convert(int(pc,2)+1)


def f_sub(l, pc):
    reg["111"] = "0000000000000000"  # Initialize register "111" with all zeros
    n1 = int(reg[l[10:13]], 2)  # Extract value of reg2
    n2 = int(reg[l[13:16]], 2)  # Extract value of reg3
    x = n1 - n2  # Perform the subtraction reg2 - reg3

    if x < 0:
        reg[reg["111"]] = "00000000"  # Write 0 to reg1
        overflow_flag = True  # Set overflow flag
    else:
        reg[reg["111"]] = bin(x)[2:].zfill(8)  # Store the result in reg1
        overflow_flag = False  # Clear overflow flag

    return convert(int(pc, 2) + 1)

def mul(l,pc):
    reg["111"] = "0000000000000000"
    n1 = int(reg[l[10:13]], 2)
    n2 = int(reg[l[13:16]], 2)
    x = (n1 * n2)
    y = bin(x)
    if len(y) > 18:
        reg[l[7:10]]=y[-16:]
        reg['111'] = convert1(int(reg['111'], 2) + 8)

    else:
        reg[l[7:10]] = convert1(x)
    return convert(int(pc,2)+1)

def div(l,pc):
    reg["111"]="0000000000000000"
    n1 = int(reg[l[10:13]], 2)
    n2 = int(reg[l[13:16]], 2)
    x = (n1 // n2)
    y = n1 % n2
    x = convert1(x)
    y = convert1(y)
    reg["000"]=x
    reg["001"]=y
    return convert(int(pc,2)+1)

def left_shift(l,pc):
    reg["111"] = "0000000000000000"
    x = int(reg[l[6:9]], 2) << int(l[9:], 2)
    x = convert1(x)
    if (len(x) > 16):
        reg['111'] = (bin(int(reg['111'], 2) + 9))[2:]
    else:
        reg[l[6:9]] = x
    return convert(int(pc,2)+1)

def right_shift(l,pc):
    reg["111"] = "0000000000000000"
    x = int(reg[l[6:9]], 2) >> int(l[9:], 2)
    x = convert1(x)
    reg[l[6:9]] = x
    return convert(int(pc,2)+1)

def xor_fnc(l,pc):
    reg["111"] = "0000000000000000"
    reg[l[7:10]] = convert1(int(reg[l[10:13]], 2) ^ int(reg[l[13:]], 2))
    return convert(int(pc,2)+1)

def or_fnc(l,pc):
    reg["111"] = "0000000000000000"
    reg[l[7:10]] = convert1(int(reg[l[10:13]], 2) | int(reg[l[13:]], 2))
    return convert(int(pc,2)+1)

def and_fnc(l,pc):
    reg["111"] = "0000000000000000"
    reg[l[7:10]] = convert1(int(reg[l[10:13]], 2) & int(reg[l[13:]], 2))

    return convert(int(pc,2)+1)
def not_fnc(l,pc):
    
    reg["111"] = "0000000000000000"
    lam=convert1(int(reg[l[13:]], 2))
    lam=lam.replace("0","2")
    lam=lam.replace("1","0")
    lam=lam.replace("2","1")
    reg[l[10:13]] = lam
    return convert(int(pc,2)+1)

def load(l,pc):
    reg["111"] = "0000000000000000"
    reg[l[6:9]] = MEM[l[9:]]
    X.append(X[-1])
    Y.append(int(l[9:], 2))
    return convert(int(pc,2)+1)

def store(l,pc):
    reg["111"] = "0000000000000000"
    MEM[l[9:]] = reg[l[6:9]]
    X.append(X[-1])
    Y.append(int(l[9:], 2))
    return convert(int(pc,2)+1)

def compare(l,pc):

    reg['111'] = '0000000000000000'
    if int(reg[l[10:13]], 2) == int(reg[l[13:]], 2):
        reg['111'] = convert1(int(reg['111'], 2) + 1)
    elif int(reg[l[10:13]], 2) > int(reg[l[13:]], 2):
        reg['111'] = convert1(int(reg['111'], 2) + 2)
    elif int(reg[l[10:13]], 2) < int(reg[l[13:]], 2):
        reg['111'] = convert1(int(reg['111'], 2) + 4)
    return convert(int(pc,2)+1)
#******

def jump_uncond(l,pc):
    return l[9:]
def jump_if_less(l,pc):
    if (reg['111'][-3] == '1'):
        return l[9:]
    else:
        return convert(int(pc, 2) + 1)


def jump_if_greater(l,pc):
    if (reg['111'][-2] == '1'):
        return l[9:]
    return convert(int(pc, 2) + 1)


def jump_if_equal(l,pc):
    if (reg['111'][-1] == '1'):
        return l[9:]
    return convert(int(pc, 2) + 1)
#********

def halt(pc):
    RF_dump()
    print()
    return pc

def PC_dump(pc):
    print(pc,end="        ")


def MEM_DUMP():
    var=1
    for i in MEM.keys():
        print(MEM[i])
        # ,"LINE =",var)var+=1


def RF_dump():
    for i in reg.keys():
        print(reg[i],end=" ")
    print()

def M(pc):
    c=0
    while(1):
    
        X.append(c)
        Y.append(int(pc, 2))
        c=c+1
        PC_dump(pc)
         
        # print("stmts",statements[pc])
        if(pc==convert(len(statements)-1)):
            RF_dump()
            break
        if (statements[pc][0:5] == "00000"):
            pc=add(statements[pc],pc)
        elif (statements[pc][0:5] == "00001"):
            pc=sub(statements[pc],pc)
        elif (statements[pc][0:5] == "00010"):
            pc=mov1(statements[pc],pc)
        elif (statements[pc][0:5] == "00011"):
            pc=mov2(statements[pc],pc)
        elif (statements[pc][0:5] == "00100"):
            pc=load(statements[pc],pc)
        elif (statements[pc][0:5] == "00101"):
            pc=store(statements[pc],pc)
        elif (statements[pc][0:5] == "00110"):
            pc=mul(statements[pc],pc)
        elif (statements[pc][0:5] == "00111"):
            pc=div(statements[pc],pc)
        elif (statements[pc][0:5] == "01000"):
            pc=right_shift(statements[pc],pc)
        elif (statements[pc][0:5] == "01001"):
            pc=left_shift(statements[pc],pc)
        elif (statements[pc][0:5] == "01010"):
            pc=xor_fnc(statements[pc],pc)
        elif (statements[pc][0:5] == "01011"):
            pc=or_fnc(statements[pc],pc)
        elif (statements[pc][0:5] == "01100"):
            pc=and_fnc(statements[pc],pc)
        elif (statements[pc][0:5] == "01101"):
            pc=not_fnc(statements[pc],pc)
        elif (statements[pc][0:5] == "01110"):
            pc=compare(statements[pc],pc)
        elif (statements[pc][0:5] == "01111"):
            pc=jump_uncond(statements[pc],pc)
        elif (statements[pc][0:5] == "11100"):
            pc=jump_if_less(statements[pc],pc)
            reg["111"] = "0000000000000000"
        elif (statements[pc][0:5] == "11101"):
            pc=jump_if_greater(statements[pc],pc)
            reg["111"] = "0000000000000000"
        elif (statements[pc][0:5] == "11111"):
            pc=jump_if_equal(statements[pc],pc)
            reg["111"] = "0000000000000000"
        elif (statements[pc][0:5] == "10000"):
            pc=f_add(statements[pc],pc)
        elif (statements[pc][0:5] == "10001"):
                    pc=f_sub(statements[pc],pc) 
        elif (statements[pc][0:5] == "10010"):
                    pc=f_mov1(statements[pc],pc)
        elif (statements[pc][0:5] == "11010"):
            pc=halt(pc)
            RF_dump()
            break
        RF_dump()
        
    MEM_DUMP()
M(pc)
