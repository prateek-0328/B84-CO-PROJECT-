
'''if regval=1 -> $Imm mov instruction
   if regval=2 -> reg mov instruction
   if ins not found  ->  return 0 '''
def opcode(ins, regval=0): 
    #returns the opcode of the instruction; returns 0 if instruction not present
    opcode={"add": "10000",
            "sub":"10001",
            "mov":["10010","10011"],
            "ld":"10100",
            "st":"10101",
            "mul":"10110",
            "div":"10111", 
            "rs":"11000",
            "ls":"11001",
            "xor":"11010",
            "or":"11011",
            "and":"11100",
            "not":"11101",
            "cmp":"11110",
            "jmp":"11111",
            "jlt":"01100",
            "jgt":"01101",
            "je":"01111",
            "hlt":"01010",
            "addf":"00000",
            "subf":"00001",
            "movf":"00010"}
    if regval==1:
        return opcode["mov"][0]
    elif regval==2:
        return opcode["mov"][1]
    for i in opcode.keys():
        if ins==i:
            return opcode[ins]
    return 0
def regaddress(reg): 
    #returns the address of a specified register: returns 0 if register not present
    regaddress={"R0":"000",
            "R1":"001",
            "R2":"010",
            "R3":"011",
            "R4":"100",
            "R5":"101",
            "R6":"110",
            "FLAGS":"111"}
    if reg in regaddress.keys():
        return( regaddress[reg])
    else:
        return 0
def instype(ins,regval=0): 
    #returns the type of instruction as a string
    typetable={"a":["add","sub","mul","xor","or","and","addf","subf"],
                "b":["mov","ls","rs","movf"],
                "c":["mov","div","not","cmp"],
                "d":["ld","st"],
                "e":["jmp","jlt","jgt","je"],
                "f":["hlt"]}
                
    if regval==1:
        return "b"
    elif regval==2:
        return "c"
    for i in typetable.keys():
        if ins in typetable[i]:
            return i
    return 0


def eightbit(num):
    #converts a number into an 8 bit binary number and returns it 
    binaryno=bin(num)[2::]
    number=(8-len(binaryno))*"0"+binaryno
    return number
from sys import stdin

      
#f=open("stdin")
linesofcode=stdin.readlines()   
#stores all the lines of the input in a list
    



binarycode=[]  #final converted binary lines are stored here
varinitstart=True  #flag variable which is true at the beginning where the variables are initiated 
halt=False #flag variable stating that the code has not been stopped yet
errors=[]   #all the errors in the code are stored here
var={}   # all the initiated variables are stored here as keys with values = their address
labels={}  # all the initiated labels are stored here as keys with values = their address
variables=0   #stores the total number of variables
mptlines=0   #stores the number of blank lines in the code

for i in linesofcode:
    if not i:
        mptlines+=1
    elif i.split()[0]=="var":
        variables+=1
    else:
        break
store=variables
count=1
    #for variable declaration
varadd=len(linesofcode)-variables-mptlines  #temp variable for the address of a variable in the code
#the variables are stored after all the instructions

while(variables):
    if (not linesofcode[0]):
        count+=1
        continue
    line= linesofcode[0].split()
    if (line[0]=="var" and len(line)==2):
        if line[1] not in var.keys():  
            var[line[1]]=eightbit(varadd)
            varadd+=1
            variables-=1
            linesofcode.pop( 0 )
            count+=1
            continue
        else:
            errors.append("ERROR at line "+ str(count)+" :Multiple declaration for the same variable found")
            count+=1
            continue

    elif(line[0]=="var"):
        errors.append("ERROR at line "+str(count+1)+" :Improper variable declaration")
        variables-=1
        linesofcode.pop(0)
        count+=1
        continue
    else:
        varinitstart=False
        break
varinitstart=False
variables=store


    #for labels
for line in range (len(linesofcode)):
    if len(linesofcode[line].split())==0:
        continue
    if (linesofcode[line].split()[0][-1]==":"):
        if linesofcode[line].split()[0][:len(linesofcode[line].split()[0])-1:] not in labels:
            labels[linesofcode[line].split()[0][:len(linesofcode[line].split()[0])-1:]]=eightbit(line)
            x=""
            for i in range(1,len(linesofcode[line].split())):
                x+=linesofcode[line].split()[i]+" "
            linesofcode[line]=x
        else:
            errors.append("ERROR at line "+str(line+variables+1)+" :Multiple declaration for the same label found")
            continue
for line in range (len(linesofcode)):
    store=linesofcode[line].split()
    if (not store):
        continue
    if (store[0]=="var" and not varinitstart):
        errors.append("ERROR at line "+str(line+variables+1)+" :Variable not declared at the beginning")
        continue
    if (store[0][-1]==":"):
        errors.append("ERROR at line "+str(line+variables+1)+" :Use of multiple labels is not supported")
        continue
    
    
    if instype(store[0])==0 and store[0]!="mov":
        errors.append("ERROR at line "+str(line+variables+1)+" :Instruction not valid")
        continue
    if halt:
        errors.append("ERROR at line "+str(line+variables+1)+" :Halt(hlt) is not the last instruction.")
        continue

    if (store[0]=="mov" and len(store)==3 and (store[2][0]=="R" or store[2]=="FLAGS")):

        if (regaddress(store[2])==0):
            errors.append("ERROR at line "+str (line +variables+1)+" :Register not valid.")
            continue
        elif(regaddress(store[2]!=0)):
            if (regaddress(store[1])==0):
                errors.append("ERROR at line "+str(line+variables+1)+" :Register not valid.")
                continue
            if (regaddress(store[1])=="111"):
                errors.append("ERROR at line "+str(line+variables+1)+" :Illegal use of flags.")
                continue
        binarycode.append(opcode(store[0],2)+"00000"+regaddress(store[1])+regaddress(store[2]))
        continue
    elif (len(store)==3 and store[0]=="mov" and store[2][0]!="R"):
        
        if regaddress(store[1]==0):
            errors.append("ERROR at line "+str(line +variables+1)+" :Register not valid")
            continue
        if regaddress(store[1])=="111":
            errors.append("ERROR at line "+str(line+variables+1)+" :Illegal use of flags")
            continue
        if store[2][0]!="$":
            errors.append("ERROR at line "+str(line+variables+1)+" :Syntax Error")
            continue
        if (int(store[2][1::]) not in range(0,256)):
            errors.append("ERROR at line "+str(line+variables+1)+" :Illegal Immediate Value ")
            continue
        binarycode.append(opcode(store[0],1)+regaddress(store[1])+eightbit(int(store[2][1::])))

        continue
    
       
    elif store[0]=="mov":
        errors.append("ERROR at line "+str(line+variables+1)+" :Wrong syntax used for instruction")
        continue


    if(instype(store[0])=="a" and len(store)==4):
        if regaddress(store[1])==0 or regaddress(store[2])==0 or regaddress(store[3])==0:
            errors.append("ERROR at line"+str(line+variables+1)+" :Invalid Register")
            continue
        if regaddress(store[1])=="111" or regaddress(store[2])=="111" or regaddress(store[3])=="111":
            errors.append("ERROR at line "+str(line +variables+1)+" :Illegal use of flags")

            continue
        binarycode.append(opcode(store[0])+"00"+regaddress(store[1])+regaddress(store[2])+regaddress(store[3]))
        continue
    elif (instype(store[0])=="a"):
        errors.append("ERROR at line "+str(line+variables+1)+" :Wrong syntax used for instruction")
        continue


    if (instype(store[0])=="b" and len(store)==3 and store[0]!="mov"):
        if store[2][0]!="$":
            errors.append("ERROR at line "+str(line +variables+1)+" :Syntax error")
            continue
        try:
            if (int(store[2][1::]) not in range (0,256)):
                errors.append("ERROR at line "+str(line+variables+1)+" Illegal Immediate value")
                continue
        except ValueError:
            errors.append("ERROR at line "+str(line+variables+1)+" Illegal Immediate value")
            continue

        if regaddress(store[1]=="111"):
            errors.append("ERROR at line "+str(line +variables+1)+" Illegal use of flags")
            continue
        if (regaddress(store[1])==0):
            errors.append("ERROR at line "+str(line+variables+1)+" Invalid register")
            continue
        binarycode.append(opcode(store[0])+regaddress(store[1])+eightbit(int(store[2][1::])))
        continue
    elif (instype(store[0])=="b" and store[0]!="mov"):

        errors.append("ERROR at line "+str(line+variables+1)+" Wrong syntax used for instruction")
        continue



    if (instype(store[0])=="c" and len(store)==3 and store[0]!="mov"):
        if regaddress(store[1]=="111" or regaddress(store[2])=="111"):
            errors.append("ERROR at line "+str(line +variables+1)+" Illegal use of flags")
            continue


        if (regaddress(store[1])==0 or regaddress(store[2])==0):
            errors.append("ERROR at line "+str(line+variables+1)+" Invalid register")
            continue
        binarycode.append(opcode(store[0])+"00000"+regaddress(store[1])+regaddress(store[2]))
        continue
    elif (instype(store[0])=="c"):
        errors.append("ERROR at line "+str(line+variables+1)+" Wrong syntax used for instruction")
        continue

    if (instype(store[0])=="d" and len(store)==3):
        if regaddress(store[1]=="111"):
            errors.append("ERROR at line "+str(line +variables+1)+" Illegal use of flags")
            continue
        if (regaddress(store[1])==0):

            errors.append("ERROR at line "+str(line+variables+1)+" Invalid register")
            continue
        if store[2] not in var.keys():
            if store[2] in labels.keys():
                errors.append("ERROR at line "+str (line+variables+1)+" Misuse of label as variable")
                continue
            else:
                errors.append("ERROR at line "+str(line +variables+1)+" Use of undefined variable")
                continue
        else:
            binarycode.append(opcode(store[0])+regaddress(store[1])+var[store[2]])
            continue
    elif (instype(store[0])=="d"):
        errors.append("ERROR at line "+str(line+variables+1)+" Wrong syntax used for instruction")
        continue



    if (instype(store[0])=="e" and len(store)==2):
        if store[1] not in labels.keys():
            if store[1] in var.keys():
                errors.append("ERROR at line "+str (line+variables+1)+" Misuse of variable as label")
                continue


            else:
                errors.append("ERROR at line "+str(line +variables+1)+" Use of undefined label")
                continue
        else:
            binarycode.append(opcode(store[0])+"000"+labels[store[1]])
            continue
    elif (instype(store[0])=="e"):
        errors.append("ERROR at line "+str(line+variables+1)+" Wrong syntax used for instruction")
        continue


    if instype(store[0])=="f" and len(store)==1:
        binarycode.append(opcode(store[0])+"00000000000")
        halt=True



    elif instype(store[0])=="f":
        errors.append("ERROR at line "+str(line +variables+1)+" Wrong syntax used for instruction")
        continue



if (not halt):
    errors.append("ERROR: No halt(hlt) instruction found")

if len(binarycode)>256:
    errors.append("ERROR: The code length exceeds the maximum capacity (256 lines)")
elif(len(errors)>0):
    print(errors[0])
else:
    for i in binarycode:
        print(i)











    


    








