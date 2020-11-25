class Empty:
    def __repr__(self):
        return "EMPTY"

class Data:
    def __init__(self,data):
        self.d = data
    def __repr__(self):
        return str(self.d)

class Instruction:
    def __init__(self,instruction,address,textLine):
        self.i = instruction
        self.a = address - 1
        self.t = textLine
    def __repr__(self):
        return f"{' '.join(self.t)} -- {self.i} -- {self.a}"

instructions = ["ADD","SUB","MUL","DIV","MOD","SET","STORE","STOREA","PRINT","GOTO","AND","OR","EQUAL","NOTEQUAL","GREATER","GREATEREQUAL","LESS","LESSEQUAL","IF","NOT","EXTEND","SHRINK","SETMEM"]

def ERROR(i,line,errName,info,Raise = True):
    print(f"{errName}:\nLine {i+1} -- {' '.join(line)}\n{info}\n")
    if Raise:
        exit()

#Load Program to Memory
def run(filename):
    memory = []

    success = True
    with open(filename,"r") as f:
        i = 0
        for line in f.readlines():
            if i >= len(memory):
                memory.append(Empty())
            line = line.split("#")[0].strip()
            line = line.replace("\n","")
            if line == "":
                i += 1
                continue
            line = line.split(" ")
            if len(line) == 1:
                try:
                    memory[i] = Data(int(line[0]))
                except ValueError:
                    if not line[0] in instructions:
                        ERROR(i,line,"VALUE ERROR","Data must be an integer",False)
                    else:
                        ERROR(i,line,"SYNTAX ERROR","Instructions must point to a memory address",False)
            elif len(line) == 2:
                if not line[0] in instructions:
                    ERROR(i,line,"INSTRUCTION ERROR",f"'{line[0]}' is not a valid instruction",False)
                    success = False
                    continue
                try:
                    address = int(line[1])
                    if address < 0:
                        raise ValueError()
                    if address >= len(memory):
                        memory += [Empty()] * (len(memory) - address)

                    memory[i] = Instruction(line[0],address,line)
                except ValueError:
                    ERROR(i,line,"VALUE ERROR","Memory address must be a positve integer",False)
                    success = False
            elif len(line) > 2:
                if line[0] != "STORE":
                    ERROR(i,line,"SYNTAX ERROR","Cannot have more than 2 pieces of infomation on a given line",False)
                    success = False
            i += 1

    if not success:
        exit()

    PC = 0
    MAR = 0
    MDR = 0
    CIR = None
    AC = 0

    def PrintMem(PC = -1,excludeEmpty = True):
        print("~~~~~~")
        for i in range(len(memory)):
            if i == PC:
                print(i+1,memory[i],"<<<<<<<<<<<<<<<")
            elif type(memory[i]) != Empty or not excludeEmpty:
                print(i+1,memory[i])
        print("~~~~~~")

    while PC < len(memory):
        MAR = PC
        MDR = memory[MAR]
        if type(MDR) == Data or type(MDR) == Empty:
            PC += 1
            continue
        CIR = MDR
        try:
            if type(memory[CIR.a]) != Data and not CIR.i in ["STORE","GOTO","IF","NOT"]:
                ERROR(PC,CIR.t,"POINTER ERROR",f"Cannot point to a memory address containing {type(memory[CIR.a]).__name__}")
            if CIR.i == "ADD":
                AC += memory[CIR.a].d
            elif CIR.i == "SUB":
                AC -= memory[CIR.a].d
            elif CIR.i == "MUL":
                AC *= memory[CIR.a].d
            elif CIR.i == "DIV":
                AC //= memory[CIR.a].d
            elif CIR.i == "MOD":
                AC = AC % memory[CIR.a].d
            elif CIR.i == "SET":
                AC = memory[CIR.a].d
            elif CIR.i == "STORE":
                memory[CIR.a] = Data(AC)
            elif CIR.i == "STOREA":
                memory[memory[CIR.a].d] = Data(AC)
            elif CIR.i == "PRINT":
                print(memory[CIR.a].d)
            elif CIR.i == "GOTO":
                if type(memory[CIR.a]) == Data:
                    PC = memory[CIR.a].d - 1
                else:
                    PC = CIR.a
                continue
            elif CIR.i == "AND":
                AC = AC and memory[CIR.a].d
            elif CIR.i == "OR":
                AC = AC or memory[CIR.a].d
            elif CIR.i == "EQUAL":
                AC = int(AC == memory[CIR.a].d)
            elif CIR.i == "NOTEQUAL":
                AC = int(AC != memory[CIR.a].d)
            elif CIR.i == "GREATER":
                AC = int(AC > memory[CIR.a].d)
            elif CIR.i == "GREATEREQUAL":
                AC = int(AC >= memory[CIR.a].d)
            elif CIR.i == "LESS":
                AC = int(AC < memory[CIR.a].d)
            elif CIR.i == "LESSEQUAL":
                AC = int(AC <= memory[CIR.a].d)
            elif CIR.i == "IF":
                if AC == 0:
                    PC = CIR.a
                    continue
            elif CIR.i == "NOT":
                AC = int(not AC)
            elif CIR.i == "EXTEND":
                memory += [Empty()] * memory[CIR.a].d
            elif CIR.i == "SHRINK":
                memory = memory[0:len(memory)-memory[CIR.a].d]
            elif CIR.i == "SETMEM":
                if memory[CIR.a].d > len(memory):
                    memory += [Empty()] * (memory[CIR.a].d - len(memory))
                else:
                    memory = memory[0:memory[CIR.a].d]
        except IndexError:
            print("Not enough memory")
        PC += 1

run("functions.quantum")
