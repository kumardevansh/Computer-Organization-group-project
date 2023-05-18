import sys
Line_Num = 1


def memory():
    global c
    var = bin(c)[2:]
    c += 1
    if(len(var) < 7):
        zeroes = 7-len(var)
        var = '0'*zeroes+var
    return var



def binary(n):
    binary_str = ""
    while True:
        quotient = n // 2
        remainder = n % 2
        binary_str = str(remainder) + binary_str
        n = quotient
        if n == 0:
            break
    num_zeros = 7 - len(binary_str)
    padding = "0" * num_zeros
    padded_binary_str = padding + binary_str
    return padded_binary_str


def ieee(num):
    pass


def Type(strlist):
    if strlist[0] == 'add' and len(strlist) == 4:
        return 'A'
    elif strlist[0] == 'sub' and len(strlist) == 4:
        return 'A'
    elif strlist[0] == 'mul' and len(strlist) == 4:
        return 'A'
    elif strlist[0] == 'div' and len(strlist) == 3:
        return 'C'
    elif strlist[0] == 'xor' and len(strlist) == 4:
        return 'A'
    elif strlist[0] == 'or' and len(strlist) == 4:
        return 'A'
    elif strlist[0] == 'and' and len(strlist) == 4:
        return 'A'
    elif strlist[0] == 'addf' and len(strlist) == 4:
        return 'A'
    elif strlist[0] == 'subf' and len(strlist) == 4:
        return 'A'
    elif strlist[0] == 'movf' and len(strlist) == 3:
        return 'B'
    elif strlist[0] == 'mov' and len(strlist) == 3:
        if strlist[2][0] == '$':
            return 'B'
        else:
            return 'C'
    elif strlist[0] == 'ld' and len(strlist) == 3:
        return 'D'
    elif strlist[0] == 'st' and len(strlist) == 3:
        return 'D'
    elif strlist[0] == 'rs' and len(strlist) == 3:
        return 'B'
    elif strlist[0] == 'ls' and len(strlist) == 3:
        return 'B'
    elif strlist[0] == 'not' and len(strlist) == 3:
        return 'C'
    elif strlist[0] == 'cmp' and len(strlist) == 3:
        return 'C'
    elif strlist[0] == 'jmp' and len(strlist) == 2:
        return 'E'
    elif strlist[0] == 'jlt' and len(strlist) == 2:
        return 'E'
    elif strlist[0] == 'jgt' and len(strlist) == 2:
        return 'E'
    elif strlist[0] == 'je' and len(strlist) == 2:
        return 'E'
    elif strlist[0] == 'hlt' and len(strlist) == 1:
        return 'F'
    else:
        sys.stdout.write(f'{Line_Num}: ERROR => Instruction not Defined\n')
        exit()



def typeA(strlist):
    ans = ''
    
    def get_register_num(reg):
        return {
            'R0': '000',
            'R1': '001',
            'R2': '010',
            'R3': '011',
            'R4': '100',
            'R5': '101',
            'R6': '110',
            'FLAGS':'111'
        }.get(reg, None)

    def get_instruction_code(instr):
        return {
            'add': '00000',
            'sub': '00001',
            'mul': '00110',
            'xor': '01010',
            'or': '01011',
            'and': '01100',
            'addf': '10000',
            'subf': '10001'
        }.get(instr, None)

    instr_code = get_instruction_code(strlist[0])

    if instr_code is None:
        sys.stdout.write(f'{Line_Num}: ERROR => Invalid Instruction\n')
        exit()
        
    else:
        ans += instr_code

    ans += '00'

    r1 = get_register_num(strlist[1])
    r2 = get_register_num(strlist[2])
    r3 = get_register_num(strlist[3])

    if r1 is None or r2 is None or r3 is None:
        sys.stdout.write(f'{Line_Num}: ERROR => Register not Defined\n')
        exit()
        
    else:
        ans += r1 + r2 + r3

    return ans


def typeB(strlist):
    register_codes = {
        'R0': '000',
        'R1': '001',
        'R2': '010',
        'R3': '011',
        'R4': '100',
        'R5': '101',
        'R6': '110',
        'FLAGS': '111',
    }

    instruction_codes = {
        'mov': '00010',
        'ls': '01001',
        'rs': '01000',
        'movf': '10010',
    }

    if strlist[0] not in instruction_codes:
        sys.stdout.write(f'{Line_Num}: ERROR => Invalid Instruction\n')
        exit()
        

    ans = instruction_codes[strlist[0]]

    r1 = strlist[1]
    if r1 not in register_codes:
        sys.stdout.write(f'{Line_Num}: ERROR => Register not Defined\n')
        exit()
        
    ans += '0' + register_codes[r1]

    if strlist[0] == 'mov' and (int(strlist[2][1:]) >= 127 or int(strlist[2][1:]) < 0):
        sys.stdout.write(f'{Line_Num}: ERROR => Number is not between 0 and 127\n')
        exit()
        
    if strlist[0] == 'movf' and (int(strlist[2][1:]) >= 252 or int(strlist[2][1:]) < 0):
        sys.stdout.write(f'{Line_Num}: ERROR => Number is not between 0 and 127\n')
        exit()
        

    ans += binary(int(strlist[2][1:])) if strlist[0] == 'mov' else ieee(str(float(strlist[2][1:])))

    return ans



def typeC(strlist):
    opcode_map = {
        'mov': '00011',
        'div': '00111',
        'not': '01101',
        'cmp': '01110'
    }
    
    register_map = {
        'R0': '000',
        'R1': '001',
        'R2': '010',
        'R3': '011',
        'R4': '100',
        'R5': '101',
        'R6': '110',
        'FLAGS':'111'
    }
    
    if strlist[0] not in opcode_map:
        sys.stdout.write(f'{Line_Num}: ERROR => Invalid Instruction\n')
        exit()
        
    
    opcode = opcode_map[strlist[0]]
    ans = opcode + '00000'
    
    if strlist[1] not in register_map:
        sys.stdout.write(f'{Line_Num}: ERROR => Register not Defined\n')
        exit()
        
    
    ans += register_map[strlist[1]]
    
    if strlist[2] not in register_map:
        sys.stdout.write(f'{Line_Num}: ERROR => Register not Defined\n')
        exit()
        
    
    ans += register_map[strlist[2]]
    
    return ans



def typeD(strlist, mem):
    def get_register_encoding(register_name):
        register_encodings = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110'}
        if register_name in register_encodings:
            return register_encodings[register_name]
        else:
            sys.stdout.write(f'{Line_Num}: ERROR => Register not Defined\n')
            exit()
            

    def encode_ld_instruction(register_name, memory_data):
        strD = '00100'
        strD += '0'
        strD += get_register_encoding(register_name)
        strD += '0'
        strD += memory_data
        return strD

    def encode_st_instruction(register_name, memory_data):
        strD = '00101'
        strD += '0'
        strD += get_register_encoding(register_name)
        strD += '0'
        strD += memory_data
        # print("memory_type",type(mem),"memory data-",mem)
        return strD

    if strlist[0] == 'ld':
        return encode_ld_instruction(strlist[1], mem[1:])
    elif strlist[0] == 'st':
        return encode_st_instruction(strlist[1], mem[1:])
    else:
        sys.stdout.write(f'{Line_Num}: ERROR => Invalid Instruction\n')
        exit()
        



def typeE(strlist, mem):
    # print(mem)
    def encode_jump_instruction(opcode):
        if opcode == 'jmp':
            return '01111'
        elif opcode == 'jlt':
            return '11100'
        elif opcode == 'jgt':
            return '11101'
        elif opcode == 'je':
            return '11111'

    label = strlist[1]
    if label not in label_arr:
        sys.stdout.write(f'{Line_Num}: ERROR => Label not Defined\n')
        exit()
        

    opcode = encode_jump_instruction(strlist[0])
    strE = opcode + '0000'
    mem = mem[1:]
    strE += mem
    # print("memory_type",type(mem),"memory data-",mem)

    return strE



def typeF(strlist):
    if strlist[0] == 'hlt':
        strF = '11010' + '0'*11
        return strF
    else:
        sys.stdout.write(f'{Line_Num}: ERROR => hlt Instruction not found\n')
        exit()
        

def memory_label():
    global c
    var = bin(c - 1)[2:]
    var = '0' * (8 - len(var)) + var if len(var) < 8 else var
    return var


def Input():
    global c
    global label_arr
    label_arr = []

    Array_Input_1 = sys.stdin.read().splitlines()

    for line in Array_Input_1:
        if line == '':
            Array_Input_1.remove(line)

    Array_Input = list(x.split() for x in Array_Input_1)

    hlt_flag = 0

    for Array_Line in Array_Input:
        if Array_Line[0][-1] == ':' and len(Array_Line) != 1 and Array_Line[1] == 'hlt':
                    if hlt_flag == 0:
                        hlt_flag = 1
                    else:
                        sys.stdout.write(
                            f'{Array_Input.index(Array_Line)+1}: ERROR => Instructions Written after "hlt" Instruction\n')
                        exit()
                    
        else:
            if Array_Line[0] == 'hlt':
                if hlt_flag == 0:
                    hlt_flag = 1
                else:
                    sys.stdout.write(
                        f'{Array_Input.index(Array_Line)+1}: ERROR => Instructions Written after "hlt" Instruction\n')
                    exit()
                    

    for Array_Line in Array_Input:
        if Array_Line[0][-1] == ':' and len(Array_Line) == 1:
            # if len(Array_Line) == 1:
                sys.stdout.write(
                    f'{Array_Input.index(Array_Line)+1}: ERROR => Invalid Instruction\n')
                exit()
                
    if Array_Input[-1][0][-1] == ':':
            if Array_Input[-1][1] != 'hlt':
                sys.stdout.write(f'{Array_Input.index(Array_Line)+1}: ERROR => Missing "hlt" Instruction in Last Line\n')
                exit()
    else:
        if Array_Input[-1][0] != 'hlt':
            sys.stdout.write(f'{Array_Input.index(Array_Line)+1}: ERROR => Missing "hlt" Instruction in Last Line\n')
            exit()
              
            

    for Array_Line in Array_Input:
        if Array_Line[0][-1] == ':':
            label_arr.append(Array_Line[0][:-1])

    for i in range(len(Array_Input)):
        if (Array_Input[i][0] != 'var'):
            c += 1
            
        
        if(Array_Input[i][0][-1] == ':'):
            d[Array_Input[i][0][:-1]] = memory_label()
            

    for i in range(len(Array_Input)):
        if(Array_Input[i][0] == 'var' and len(Array_Input[i]) == 2):

            d[Array_Input[i][1]] = memory()

    return Array_Input

def Output(Array_Input):
    global Line_Num
    global Array_Var

    Array_Var = []
    Array_Output = []

    flag = 0

    for Array_Line in Array_Input:
        if len(Array_Line) > 5:
            sys.stdout.write(f'{Line_Num}: ERROR => Invalid Instruction\n')
            exit()
            

        if Array_Line[0] == 'var':
            if len(Array_Line) == 2:
                if flag == 0:
                    Array_Var.append(Array_Line[1])
                else:
                    sys.stdout.write(
                        f'{Line_Num}: ERROR => Variable Not Declared in Beginning\n')
                    exit()
                    
            else:
                sys.stdout.write(f'{Line_Num}: ERROR => Invalid Instruction\n')
                exit()
                
        else:
            flag = 1


        
        if Array_Line[0] != 'var' and Array_Line[0][-1] != ':':
            ins_type = Type(Array_Line)
            lst_alpha=['A','B','C','D','E','F']
            lst_num=[4,3,2,1]
            k=10
            l=11
            my_dict={} 
            my_dict[k]=ins_type
            my_dict[l]=len(Array_Line)
            
            if my_dict[k] == lst_alpha[3]:
                if my_dict[l] == lst_num[1]:
                    if Array_Line[2] in Array_Var:
                        Array_Output.append(typeD(Array_Line, d[Array_Line[2]]))
                        
            elif my_dict[k] == lst_alpha[4] :
                if my_dict[l] == lst_num[2] :
                    if Array_Line[1] in label_arr:
                        Array_Output.append(typeE(Array_Line, d[Array_Line[1]]))
                        
            elif my_dict[k]==lst_alpha[0] :
                if my_dict[l] == lst_num[0]:
                    Array_Output.append(typeA(Array_Line))
            elif my_dict[k] == lst_alpha[1] :
                if my_dict[l] == lst_num[1]:
                    Array_Output.append(typeB(Array_Line))
            elif my_dict[k] == lst_alpha[2] :
                if my_dict[l] == lst_num[1]:
                    Array_Output.append(typeC(Array_Line))
            elif my_dict[k] == lst_alpha[5] :
                if my_dict[l] == lst_num[3]:
                    Array_Output.append(typeF(Array_Line))
            else:
                sys.stdout.write(f'{Line_Num}: ERROR => Invalid Instruction\n')
                exit()
                

        if Array_Line[0] != 'var' and Array_Line[0][-1] == ':':
            ins_type = Type(Array_Line[1:])
            lst_alpha=['A','B','C','D','E','F']
            lst_num=[5,4,3,2]
            my_dict1={}
            k=10
            l=11
            my_dict1[k]=ins_type
            my_dict1[l]=len(Array_Line)
            if my_dict1[k] == lst_alpha[3] :
                if my_dict1[l] == lst_num[1] :
                    if Array_Line[3] in Array_Var:
                        Array_Output.append(typeD(Array_Line[1:], d[Array_Line[3]]))
                        
            elif my_dict1[k] == lst_alpha[4] :
                if my_dict1[l] == lst_num[2] :
                    if Array_Line[2] in label_arr:
                        Array_Output.append(typeE(Array_Line[1:], d[Array_Line[2]]))
                        
            elif my_dict1[k] == lst_alpha[0] :
                if my_dict1[l] == lst_num[0]:
                    Array_Output.append(typeA(Array_Line[1:]))
            elif my_dict1[k] == lst_alpha[1] :
                if my_dict1[l] == lst_num[1]:
                    Array_Output.append(typeB(Array_Line[1:]))
            elif my_dict1[k] == lst_alpha[2] :
                if  my_dict1[l] == lst_num[1]:
                    Array_Output.append(typeC(Array_Line[1:]))
            elif my_dict1[k] == lst_alpha[5] :
                if  my_dict1[l] == lst_num[3]:
                    Array_Output.append(typeF(Array_Line[1:]))
            else:
                sys.stdout.write(f'{Line_Num}: ERROR => Invalid Instruction\n')
                exit()
                

        Line_Num += 1

    return Array_Output


c = 0
global d
d = dict()

Array_Input = Input()

Array_Output = Output(Array_Input)

for x in Array_Output:
    sys.stdout.write(x)
    sys.stdout.write('\n')
