from sys import stdin
# utility functions
def sixteenbit(num):
    #converts a number into an 16 bit binary number and returns it 
    binaryno=bin(num)[2::]
    number=(16-len(binaryno))*"0"+binaryno
    return number
def eightbit(num):
    #converts a number into an 8 bit binary number and returns it 
    binaryno=bin(num)[2::]
    number=(8-len(binaryno))*"0"+binaryno
    return number
def overflow(num):
    #checks if the value of the register exceeds the range of the registers
    if (num>2**16-1):
        return True
    else:
        return False
def integer(num):
    # converts binary eight bit value to their respective integer values.

    return int(num,2)
# ----------------------------------------------------------------------------------
# register file 

reg={       "000":0,
            "001":0,
            "010":0,
            "011":0,
            "100":0,
            "101":0,
            "110":0,
            }
flag="0000000000000000"
def rfdump(reg,flag):
    for i in reg.keys():
        print(sixteenbit(reg[i]),end=" ")
    print(flag)

def setflag(flag,operation):
    if operation==0:
   # resets the  flag register to default value to be used after every instruction
        flag="0000000000000000"
    elif operation==1:
        # Sets the Overflow(V) flag: 3rd bit to 1
        flag="0000000000001000"
    elif operation==2:
        # Sets the Less Than(L) flag: 2nd bit to 1
        flag="0000000000000100"
    elif operation==3:
        # Sets the Greater Than(G) flag: 1st bit to 1
        flag="0000000000000010"
    else:
        # Sets the Equals(G) flag: 0th bit to 1
        flag="0000000000000001"
def getflag(flag):
    print(flag, end=" ")


def setregister(reg,address,val):
    if not overflow(val):
        reg[address]=val
    else:
        rbin = bin(val)[2::]
        reg[address] = int(rbin[len(rbin)-16::], 2)
def getregister(reg,flag,address,bindec):
    if bindec:
        if address=="111":
            return flag
        rbin=bin(reg[address])[2::]
        if len(rbin)>16:
            return rbin[len(rbin)-16::]
        else:
            return sixteenbit(reg[address])
    else:
        if address=="111":
            return int (flag,2)
        return reg[address]

# ---------------------------------------------------------------
# program counter

counter=0
def pcdump(counter):
    print(eightbit(counter),end=" ")

# ---------------------------------------------------------------
# memory

mem=[]
xcoord=[]
ycoord=[]
cycle=0

def start():
    for line in stdin:
        mem.append(line[0:16:])
    if len(mem)<256:
        empty=256-len(mem)
        for i in range(empty):
            mem.append("0000000000000000")
def data(currpc):
    return mem[currpc]
def getval(memadd):
    return int(mem[integer(memadd)],2)
def setval(memadd,val):
    mem[integer(memadd)]=sixteenbit(val)
def memdump():
    for i in mem:
        print(i)
def plotMemoryAccessTrace():
    from matplotlib import pyplot as plt
    plt.scatter(xcoord,ycoord)
    plt.ylabel("Memory Address")
    plt.xlabel("Cycle Number")
    plt.savefig("MemoryAccessTracing.png")

# --------------------------------------------------------------------
#  Execution Engine

def execute(ins):
    # takes a 16 bit binary string of assembly instructionand returns the updated state of halted ins and updated value of pc

    opcode=ins[:5:]
    #appending the point for memrory access trace
    xcoord.append(cycle)
    ycoord.append(counter)

    if opcode=="10000":
        # add unused reg1 reg2 reg3
        # 5   2      3    3    3
        R1=ins[7:10:]
        R2=ins[10:13:]
        R3=ins[13:16:]
        pR1=getregister(reg,flag,R2,False)+getregister(reg,flag,R3,False)
        if overflow(pR1):
            setflag(flag,1)
        else:
            setflag(flag,0)
        setregister(reg,R1,pR1)
        halt=False
        newpc=counter+1

    elif opcode=="10001":
        # sub unused reg1 reg2 reg3
        # 5   2      3    3    3
        R1=ins[7:10:]
        R2=ins[10:13:]
        R3=ins[13:16:]
        pR1=getregister(reg,flag,R2,False)-getregister(reg,flag,R3,False)
        if pR1 <0:
            setflag(flag,1)
            setregister(reg,R1,0)
        else:
            setregister(reg,R1,pR1)
            setflag(flag,0)
        halt=False
        newpc=counter+1
    
    elif opcode=="10010":
        # mov reg1 $Imm
        # 5   3    8
        R1=ins[5:8:]
        val=integer(ins[8::])
        setregister(reg,R1,val)
        setflag(flag,0)
        halt=False
        newpc=counter+1
    
    elif opcode=="10011":
        # mov unused reg1 reg2
        # 5   5      3    3
        R1=ins[10:13:]
        R2=ins[13::]
        setregister(reg,R1,getregister(reg,flag,R2,False))
        setflag(flag,0)
        halt=False
        newpc=counter+1

    elif opcode=="10100":
        # ld reg1 mem_addr
        # 5  3    8
        R1=ins[5:8:]
        memadd=ins[8::]
        xcoord.append(cycle)
        ycoord.append(integer(memadd))
        val=getval(memadd)
        setregister(reg,R1,val)
        setflag(flag,0)
        halt=False
        newpc=counter+1

    elif opcode=="10101":
        # st reg1 mem_addr
        # 5  3    8
        R1=ins[5:8:]
        memadd=ins[8::]
        xcoord.append(cycle)
        ycoord.append(integer(memadd))
        setval(memadd,getregister(reg,R1,False))
        setflag(flag,0)
        halt=False
        newpc=counter+1

    elif opcode=="10110":
        # mul unused reg1 reg2 reg3
        # 5   2      3    3    3
        R1=ins[7:10:]
        R2=ins[10:13:]
        R3=ins[13:16:]
        pR1=getregister(reg,flag,R2,False)*getregister(reg,flag,R3,False)
        if overflow(pR1):
            setflag(flag,1)
        else:
            setflag(flag,0)
        setregister(reg,R1,pR1)
        halt=False
        newpc=counter+1

    elif opcode=="10111":
        # div unused reg1 reg2
        # 5   5      3    3   
        R1=ins[10:13:]
        R2=ins[13::]
        rem=getregister(reg,R1,False)%getregister(reg,R2,False)
        quotient=getregister(reg,R1,False)//getregister(reg,R2,False)
        setregister(reg,"000",quotient)
        setregister(reg,"111",rem)
        setflag(flag,0)
        halt=False
        newpc=counter+1

    elif opcode=="11000":
        # rs reg1 $Imm
        # 5  3    8
        R1=ins[5:8:]
        val=integer(ins[8::])
        shifteds='0'*val+getregister(reg,R1,True)[:len(getregister(reg,R1,True))-val:]
        setregister(reg,R1,int(shifteds,2))
        setflag(flag,0)
        halt=False
        newpc=counter+1
    
    elif opcode=="11001":
        # ls reg1 $Imm
        # 5  3    8
        R1=ins[5:8:]
        val=integer(ins[8::])
        shifteds=getregister(reg,R1,True)[val::]+'0'*val
        setregister(reg,R1,int(shifteds,2))
        setflag(flag,0)
        halt=False
        newpc=counter+1
    
    elif opcode=="11010":
        # xor unused reg1 reg2 reg3
        # 5   2      3    3    3
        R1=ins[7:10:]
        R2=ins[10:13:]
        R3=ins[13::]
        pR1=getregister(reg,flag,R2,False)^getregister(reg,flag,R3,False)
        setregister(reg,R1,pR1)
        setflag(flag,0)
        halt=False
        newpc=counter+1

    elif opcode=="11011":
        # or unused reg1 reg2 reg3
        # 5  2      3    3    3
        R1=ins[7:10:]
        R2=ins[10:13:]
        R3=ins[13::]
        pR1=getregister(reg,flag,R2,False)|getregister(reg,flag,R3,False)
        setregister(reg,R1,pR1)
        setflag(flag,0)
        halt=False
        newpc=counter+1

    elif opcode=="11100":
        # and unused reg1 reg2 reg3
        # 5   2      3    3    3
        R1=ins[7:10:]
        R2=ins[10:13:]
        R3=ins[13::]
        pR1=getregister(reg,flag,R2,False)&getregister(reg,flag,R3,False)
        setregister(reg,R1,pR1)
        setflag(flag,0)
        halt=False
        newpc=counter+1
    
    elif opcode=="11101":
        # not unused reg1 reg2
        # 5   5      3    3
        R1=ins[10:13:]
        R2=ins[13::]
        inverted=""
        for i in R2:
            if i=="1":
                inverted+="0"
            else:
                inverted+="1"
        setregister(reg,R1,int(inverted,2))
        setflag(flag,0)
        halt=False
        newpc=counter+1
    
    elif opcode=="11110":
        # cmp unused reg1 reg2
        # 5   5      3    3
        R1=ins[10:13:]
        R2=ins[13::]
        if getregister(reg,R1,False)<getregister(reg,R2,False):
            setflag(flag,2)
        elif getregister(reg,R1,False)>getregister(reg,R2,False):
            setflag(flag,3)
        else:
            setflag(flag,4)
        halt=False
        newpc=counter+1
    
    elif opcode=="11111":
        # jmp unused mem_addr
        # 5   3      8
        memadd=ins[8::]
        newpc=integer(memadd)
        setflag(flag,0)
        halt=False
        
    
    elif opcode=="01100":
        # jlt unused mem_addr
        # 5   3      8
        if flag=="0000000000000100":
            memadd=ins[8::]
            newpc=integer(memadd)
            halt=False
        else:
            halt=False
            newpc=counter+1
        setflag(flag,0)
    
    elif opcode=="01101":
        # jgt unused mem_addr
        # 5   3      8
        if flag=="0000000000000010":
            memadd=ins[8::]
            newpc=integer(memadd)
            halt=False
        else:
            halt=False
            newpc=counter+1
        setflag(flag,0)


    elif opcode=="01111":
        # je unused mem_addr
        # 5  3      8
        if flag=="0000000000000001":
            memadd=ins[8::]
            newpc=integer(memadd)
            halt=False
        else:
            halt=False
            newpc=counter+1
        setflag(flag,0)

    elif opcode=="01010":
        # hlt unused
        # 5   11
        setflag(flag,0)
        halt=True
        newpc=counter+1

    cycle+=1
    return(halt,newpc)
# -----------------------------------------------------------------------------
#  main simulator 

start()                   #Load memory from stdin
halted=False

while(not halted):
    ins=data(counter)
    halted,newpc=execute(ins)
    pcdump(counter)
    rfdump(reg,flag)
    counter=newpc
memdump()
plotMemoryAccessTrace()








        
        
        





