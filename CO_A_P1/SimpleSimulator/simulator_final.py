# import sys
Lst1=[]
Lst2=[]

def bin_16(a):
    bnr = bin(a)[2:]
    res=''
    klen=len(bnr)-1
    while klen>=0:
        res+=bnr[klen]
        klen-=1
    for bis in range(16-len(res)):
        res += '0'
    
    bnr=''
    klen=len(res)-1
    while klen>=0:
        bnr+=res[klen]
        klen-=1
    return bnr

def bin_8(a):
    bnr = bin(a)[2:]
    res=''
    klen=len(bnr)-1
    while klen>=0:
        res+=bnr[klen]
        klen-=1
    for bis in range(7- len(res)):
        res += '0'
    bnr=''
    klen=len(res)-1
    while klen>=0:
        bnr+=res[klen]
        klen-=1
    return bnr

v1 = 0

Lines = {}

count_pc ="0000000"
reg = {'000': "0000000000000000",'001': "0000000000000000",'010': "0000000000000000",'011': "0000000000000000",'100': "0000000000000000",'101': "0000000000000000",'110': "0000000000000000",'111': "0000000000000000"}

while (1):
    try:
        line = input()
        if(line!=""):
            Lines[bin_8(v1)] = line
            v1 += 1
    except EOFError:
        break
MEM = Lines.copy()
MEM_len = len(MEM)
while (MEM_len <= 127):
    MEM[bin_8(MEM_len)] = "0000000000000000"
    MEM_len+=1

def mov1(inp,count_pc):
    regmov=[]
    regmov.append("0000000000000000")
    reg["111"]="0000000000000000"
    if regmov[0][0]=='0':
        regmov.append("0000000000000000")
    else:
        regmov.remove("0000000000000000")
    reg[inp[6:9]]=bin_16(int(inp[9:], 2))
    mov=regmov[0]
    regmov.append(mov)
    return bin_8(int(count_pc,2)+1)

def f_mov1(inp,count_pc):
    regfmov=[]
    regfmov.append("0000000000000000")
    if regfmov[0][0]=='0':
        regfmov.append("0000000000000000")
    else:
        regfmov.remove("0000000000000000")
    reg["111"]="0000000000000000"
    reg[inp[5:8]]=bin_16(int(inp[8:], 2))
    fmov=regfmov[0]
    regfmov.append(fmov)
    return bin_8(int(count_pc,2)+1)


def mov2(inp,count_pc):
    regmov=[]
    regmov.append("0000000000000000")
    if regmov[0][0]=='0':
        regmov.append("0000000000000000")
    else:
        regmov.remove("0000000000000000")
    reg[inp[10:13]]=bin_16(int(reg[inp[13:]],2))
    reg["111"]="0000000000000000"
    mov=regmov[0]
    regmov.append(mov)
    return bin_8(int(count_pc,2)+1)


def add(inp,count_pc):
    regadd=[]
    reg["111"] = "0000000000000000"
    regadd.append("0000000000000000")
    for i in regadd[0]:
        regadd.append(i)
    num1 = int(reg[inp[10:13]], 2)
    num2 = int(reg[inp[13:16]], 2)
    regadd.append(num1)
    regadd.append(num2)
    res = (num1 + num2)
    res2 = (num1 + num2)
    res2 = bin(res)
    regadd.remove("0000000000000000")
    if len(res2) > 18:
        reg[inp[7:10]] = res2[-16:]
        reg['111'] = bin_16(int(reg['111'], 2) + 8)
        regadd.remove(num1)
    else:
        reg[inp[7:10]] = bin_16(res)
        regadd.remove(num2)
    return bin_8(int(count_pc, 2) + 1)



def f_add(inp, count_pc):
    reg["111"] = "0000000000000000"
    num1 = int(reg[inp[10:13]], 2)  
    num2 = int(reg[inp[13:16]], 2)  
    res = num1 + num2

    if res >= 256:
        overflow_flag = True
        reg[inp[7:10]] = '00000000' 
    else:
        overflow_flag = False
        reg[inp[7:10]] = bin(res)[2:].zfill(8)

    return bin_8(int(count_pc, 2) + 1)

def sub(inp,count_pc):
    regsub=[]
    reg["111"] = "0000000000000000"
    regsub.append("0000000000000000")
    for i in regsub[0]:
        regsub.append(i)
    reg["111"] = "0000000000000000"
    num1 = int(reg[inp[10:13]], 2)
    num2 = int(reg[inp[13:16]], 2)
    regsub.append(num1)
    regsub.append(num2)
    res2 = (num1 - num2)
    res = (num1 - num2)
    if res < 0:
        reg[inp[7:10]] ="0000000000000000"
        reg['111'] = bin_16(int(reg['111'], 2) + 8)
        regsub.remove(num1)
    else:
        reg[inp[7:10]] = bin_16(res)
        regsub.remove(num2)
    return bin_8(int(count_pc,2)+1)


def f_sub(inp, count_pc):
    reg["111"] = "0000000000000000" 
    num1 = int(reg[inp[10:13]], 2)  
    num2 = int(reg[inp[13:16]], 2)  
    res = num1 - num2  

    if res < 0:
        reg[reg["111"]] = "00000000"  
        overflow_flag = True  
    else:
        reg[reg["111"]] = bin(res)[2:].zfill(8) 
        overflow_flag = False

    return bin_8(int(count_pc, 2) + 1)

def mul(inp, count_pc):
    reg["111"] = "0000000000000000"
    regmull=[]
    regmull.append("0000000000000000")
    # num1 = int(reg[inp[10:13]], 2)
    # num2 = int(reg[inp[13:16]], 2)
    res = int(reg[inp[10:13]], 2) * int(reg[inp[13:16]], 2)
    res2 = bin(res)[2:].zfill(16)
    reg[inp[7:10]] = res2[-16:]
    reg['111'] = bin(int(reg['111'], 2) + 8)[2:].zfill(16) if len(res2) > 18 else "0000000000000000"
    return bin(int(count_pc, 2) + 1)[2:].zfill(16)


def div(inp, count_pc):
    reg["111"] = "0000000000000000"
    regdiv=[]
    regdiv.append("0000000000000000")
    num1 = int(reg[inp[10:13]], 2)
    num2 = int(reg[inp[13:16]], 2)
    res = num1 // num2
    res2 = num1 % num2
    for i in regdiv[0]:
        regdiv.append(i)
    reg["000"] = bin(res)[2:].zfill(16)
    reg["001"] = bin(res2)[2:].zfill(16)
    # reg["000"] = res1
    regdiv.append(num2)
    # reg["001"] = res2
    return bin(int(count_pc, 2) + 1)[2:].zfill(16)


def ls(inp,count_pc):
    reg["111"] = "0000000000000000"
    regdiv=[]
    regdiv.append("0000000000000000")
    res = int(reg[inp[6:9]], 2) << int(inp[9:], 2)
    res = bin_16(res)
    if (len(res) > 16):
        reg['111'] = (bin(int(reg['111'], 2) + 9))[2:]
    else:
        reg[inp[6:9]] = res
    for i in regdiv[0]:
        regdiv.append(i)
    return bin_8(int(count_pc,2)+1)

def rs(inp,count_pc):
    regdiv=[]
    regdiv.append("0000000000000000")
    reg["111"] = "0000000000000000"
    res = int(reg[inp[6:9]], 2) >> int(inp[9:], 2)
    for i in regdiv[0]:
        regdiv.append(i)
    res = bin_16(res)
    reg[inp[6:9]] = res
    return bin_8(int(count_pc,2)+1)

def addi(l, count_pc):
    reg["111"] = "0000000000000000"
    n1 = int(reg[l[10:13]], 2)
    y=bin(x)
    immediate = int(l[13:16], 2)
    x = (n1 + immediate)
    if len(y) > 18:
        reg[l[7:10]] = y[-16:]
        reg['111'] = bin_16(int(reg['111'], 2) + 8)
    else:
        reg[l[7:10]] = bin_16(x)
    return bin_8(int(count_pc, 2) + 1)

def subi(l, count_pc):
    reg["111"] = "0000000000000000"
    n1 = int(reg[l[10:13]], 2)
    immediate = int(l[13:16], 2)
    x = (n1 - immediate)
    if x < 0:
        reg[l[7:10]] = "0000000000000000"
        reg['111'] = bin_16(int(reg['111'], 2) + 8)
    else:
        reg[l[7:10]] = bin_16(x)
    return bin_8(int(count_pc, 2) + 1)


def reset():
    global reg
    reg = {
        '000': '0000000000000000',
        '001': '0000000000000000',
        '010': '0000000000000000',
        '011': '0000000000000000',
        '100': '0000000000000000',
        '101': '0000000000000000',
        '110': '0000000000000000',
        '111': '0000000000000000'
    }

def inc(l, count_pc):
    n1 = int(reg[l[10:13]], 2)
    result = n1 + 1
    reg[l[7:10]] = bin_16(result)
    return bin_8(int(count_pc, 2) + 1)

def dec(l, count_pc):
    n1 = int(reg[l[10:13]], 2)
    result = n1 - 1
    reg[l[7:10]] = bin_16(result)
    return bin_8(int(count_pc, 2) + 1)
#************************************************************
#all logical fnc
def logical_bin(a):
    bnr = bin(a)[2:]
    bnr = bnr.zfill(16)
    return bnr[::-1]

def xorf(inp, count_pc):
    reg["111"] = "0000000000000000"
    operand1 = int(reg[inp[10:13]], 2)
    operand2 = int(reg[inp[13:]], 2)
    result = operand1 ^ operand2
    reg[inp[7:10]] = logical_bin(result)
    return logical_bin(int(count_pc, 2) + 1)

def orf(inp, count_pc):
    reg["111"] = "0000000000000000"
    operand1 = int(reg[inp[10:13]], 2)
    operand2 = int(reg[inp[13:]], 2)
    result = operand1 | operand2
    reg[inp[7:10]] = logical_bin(result)
    return logical_bin(int(count_pc, 2) + 1)

def andf(inp, count_pc):
    reg["111"] = "0000000000000000"
    operand1 = int(reg[inp[10:13]], 2)
    operand2 = int(reg[inp[13:]], 2)
    result = operand1 & operand2
    reg[inp[7:10]] = logical_bin(result)
    return logical_bin(int(count_pc, 2) + 1)

def notf(inp, count_pc):
    reg["111"] = "0000000000000000"
    operand = reg[inp[13:]]
    result = ''.join('1' if bit == '0' else '0' for bit in operand)
    reg[inp[10:13]] = result
    return logical_bin(int(count_pc, 2) + 1)
#***************************************************************************
def ld(inp, count_pc):
    reg["111"] = "0000000000000000"
    register = inp[6:9]
    memory_address = inp[9:]
    reg[register] = MEM[memory_address]
    Lst1.append(Lst1[-1])
    Lst2.append(int(memory_address, 2))
    return bin_8(int(count_pc, 2) + 1)

def str(inp, count_pc):
    reg["111"] = "0000000000000000"
    register = inp[6:9]
    memory_address = inp[9:]
    MEM[memory_address] = reg[register]
    Lst1.append(Lst1[-1])
    Lst2.append(int(memory_address, 2))
    return bin_8(int(count_pc, 2) + 1)

def cmp(inp, count_pc):
    reg['111'] = '0000000000000000'
    operand1 = int(reg[inp[10:13]], 2)
    operand2 = int(reg[inp[13:]], 2)
    
    if operand1 == operand2:
        reg['111'] = bin_16(int(reg['111'], 2) + 1)
    elif operand1 > operand2:
        reg['111'] = bin_16(int(reg['111'], 2) + 2)
    elif operand1 < operand2:
        reg['111'] = bin_16(int(reg['111'], 2) + 4)
    
    return bin_8(int(count_pc, 2) + 1)

#***************************************************
def jmp(inp):
    return inp[9:]
def jlt(inp,count_pc):
    if (reg['111'][-3] == '1'):
        return inp[9:]
    else:
        return bin_8(int(count_pc, 2) + 1)


def jgt(inp,count_pc):
    if (reg['111'][-2] == '1'):
        return inp[9:]
    return bin_8(int(count_pc, 2) + 1)


def je(inp,count_pc):
    if (reg['111'][-1] == '1'):
        return inp[9:]
    return bin_8(int(count_pc, 2) + 1)
#***************************************************

def count_pc_ret(count_pc):
    print(count_pc,end="        ")

def MEM_ret():
    # v1=1
    for i in MEM.keys():
        print(MEM[i])
        # v1+=1

def RF():
    for i in reg.keys():
        print(reg[i],end="        ")
    print()

def halt(count_pc):
    RF()
    print()
    return count_pc

def main_prog(count_pc):
    c = 0
    while True:
        Lst1.append(c)
        Lst2.append(int(count_pc, 2))
        c += 1
        count_pc_ret(count_pc)
        bin_op = Lines[count_pc][0:5]
        if(count_pc==bin_8(len(Lines)-1)):
            RF()
            break
        if bin_op == "00000":
            count_pc = add(Lines[count_pc], count_pc)
        elif bin_op == "00001":
            count_pc = sub(Lines[count_pc], count_pc)
        elif bin_op == "00110":
            count_pc = mul(Lines[count_pc], count_pc)
        elif bin_op == "00111":
            count_pc = div(Lines[count_pc], count_pc)
        elif bin_op == "00010":
            count_pc = mov1(Lines[count_pc], count_pc)
        elif bin_op == "00011":
            count_pc = mov2(Lines[count_pc], count_pc)
        elif bin_op == "00100":
            count_pc = ld(Lines[count_pc], count_pc)
        elif bin_op == "00101":
            count_pc = str(Lines[count_pc], count_pc)
        elif bin_op == "01110":
            count_pc = cmp(Lines[count_pc], count_pc)
        elif bin_op == "01000":
            count_pc = rs(Lines[count_pc], count_pc)
        elif bin_op == "01001":
            count_pc = ls(Lines[count_pc], count_pc)
        elif bin_op == "01010":
            count_pc = xorf(Lines[count_pc], count_pc)
        elif bin_op == "01011":
            count_pc = orf(Lines[count_pc], count_pc)
        elif bin_op == "01100":
            count_pc = andf(Lines[count_pc], count_pc)
        elif bin_op == "01101":
            count_pc = notf(Lines[count_pc], count_pc)
        elif bin_op == "10000":
            count_pc = f_add(Lines[count_pc], count_pc)
        elif bin_op == "10001":
            count_pc = f_sub(Lines[count_pc], count_pc)
        elif bin_op == "10010":
            count_pc = f_mov1(Lines[count_pc], count_pc)
        elif (Lines[count_pc][0:5] == "10011"):
            count_pc = addi(Lines[count_pc], count_pc)
        elif (Lines[count_pc][0:5] == "10100"):
            count_pc = subi(Lines[count_pc], count_pc)
        elif (Lines[count_pc][0:5] == "10101"):
            count_pc = reset()
        elif (Lines[count_pc][0:5] == "10110"):
            count_pc = inc(Lines[count_pc], count_pc)
        elif (Lines[count_pc][0:5] == "10111"):
            count_pc = dec(Lines[count_pc], count_pc)
        elif bin_op == "01111":
            count_pc = jmp(Lines[count_pc])
            # reg["111"] = "0000000000000000"
        elif bin_op == "11100":
            count_pc = jlt(Lines[count_pc], count_pc)
            reg["111"] = "0000000000000000"
        elif bin_op == "11101":
            count_pc = jgt(Lines[count_pc], count_pc)
            reg["111"] = "0000000000000000"
        elif bin_op == "11111":
            count_pc = je(Lines[count_pc], count_pc)
            reg["111"] = "0000000000000000"
        elif bin_op == "11010":
            count_pc = halt(count_pc)
            RF()
            break
        RF()

    MEM_ret()
main_prog(count_pc)
