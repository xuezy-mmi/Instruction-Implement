#import numpy as np

'''
-memory
---32-bit address
---8-bit cell

-register
---32 32-bit

-program
---add the number in memory address 0 and 1 to address 3

Assembly instruction:
---load r1 #0     000000000000 00000 000 00001 0000011   I-TYPE  lb r1, offset(0)
---load r2 #1     000000000000 00001 000 00010 0000011   I-TYPE  lb r2, offset(1)
---add r3 r2 r1   0000000 00001 00010 000 00011 0110011  R-TYPE  add r3, r2, r1
---store r3 #3    0000000 00011 00011 000 00000 0100011  S-TYPE  sb r3, offest(3)

mem3 = mem0 + mem1
'''

def List2Num(list, len):
    num = 0
    for i in range(0, len):
        num = num + list[len - 1 - i] * 2 ** i
    if(list[0] == 1):#   <0
        num = -(2 ** len - num)
    return num

def Num2List(num, len):
    list = []
    if (num >= 0):
        complement = bin(num).split('b')[1].zfill(len)
        for i in range(0,len):
            #a = int(complement[len-1-i])
            list.append(int(complement[i]))
    else :#num < 0
        '''
        num = 2 ** len + num
        num1 = bin(num).split('b')[1].zfill(len)
        snum = bin(num).split('b')[1]
        for k in range(0, len-1-len(snum)):
            list.append(1)
        for j in range(len-1-len(snum), len):
            a = int(num1[j])
            list.append(a)
        #b = '1' * (len - 1 - len(num))
        '''
        list.append(1)
        abs_num = -num
        source = bin(abs_num).split('b')[1].zfill(len-1)
        inverse = source.replace('1', 'z').replace('0', '1').replace('z', '0').replace('One', '1')
        complement = bin(int(inverse[1:], 2) + 1).split('b')[1].zfill(len-1)
        for i in range(0,len-1):
            #a = int(complement[len-2-i])
            list.append(int(complement[i]))
            
    return list

class cpu:
    def __init__(self , reg_width, reg_addr_width, mem_width, mem_addr_width, endian):
        self.pc = 0
        self.reg_width = reg_width
        self.reg_addr_width = reg_addr_width
        self.mem_width = mem_width
        self.mem_addr_width = mem_addr_width
        self.reg = [[0] * reg_width] * reg_addr_width#############################
        self.mem = [[0] * mem_width] * mem_addr_width#############################
        self.endian = endian #0:little endian 1:big-endian

    def store_mem(self, addr, data):
        mem_list = Num2List(data, self.mem_width)
        int_addr = List2Num(addr, self.mem_addr_width)
        self.mem[int_addr] = mem_list

    def display_reg(self, d, s):
        print("reg%d - reg%d : "%(d, s))
        for i in range(d,s):
            regnum = List2Num(self.reg[i], self.reg_width)
            print(self.reg[i], " number in this reg is %d" %regnum)
    def display_mem(self, d, s):
        print("mem%d - mem%d : "%(d, s))
        for i in range(d,s):
            memnum = List2Num(self.mem[i], self.mem_width)
            print(self.mem[i], " number in this mem is %d" %memnum)

def Decode(inst):
    #OP = [lb, add, sb]
    #op = [op, r1, r2, r3]
    op = [0, 0, 0, 0]
    if (inst == [0]*32):
        op = [0, 0, 0, 0]
    if (inst[25:32] == [0,0,0,0,0,1,1]):#lb
        op[0] = 1
        if (inst[17:20] == [0,0,0]):
            imm = List2Num(inst[0:12], 12)
            r1 = List2Num(inst[20 : 25], 5)
            op[1] = r1
            r2 = List2Num(inst[12 : 17], 5)
            op[2] = r2+imm
    if (inst[25:32] == [0,1,1,0,0,1,1]):#add
        op[0] = 2
        if(inst[0:7] == [0,0,0,0,0,0,0] and inst[17:20] == [0,0,0]):
            r1 = List2Num(inst[20:25],5)
            op[1] = r1
            r2 = List2Num(inst[7: 12], 5)
            op[2] = r2
            r3 = List2Num(inst[12: 17], 5)
            op[3] = r3
    if (inst[25:32] == [0,1,0,0,0,1,1]):#sb
        op[0] = 3
        if(inst[17:20] == [0,0,0]):
            imm = List2Num(inst[0:7]+inst[20:25],12)
            r1 = List2Num(inst[7:12], 5)
            op[1] = r1
            r2 = List2Num(inst[12:17], 5)
            op[2] = r2 + imm

    return op


def Op_LB(cpu, op):
    target_reg_addr = op[1]
    source_mem_addr = op[2]#   #x -> 4*x,4*x+1,4*x+24*x+3
    '''
    addr0 = source_mem_addr*4
    addr1 = source_mem_addr*4+1
    addr2 = source_mem_addr*4+2
    addr3 = source_mem_addr*4+3
    if(cpu.endian == 0):#little endian
        data = cpu.mem[addr3] + cpu.mem[addr2] + cpu.mem[addr1] + cpu.mem[addr0]#8list * 4
    else:#big endian
        data = cpu.mem[addr0] + cpu.mem[addr1] + cpu.mem[addr2] + cpu.mem[addr3]#8list * 4
    '''
    data = [0] * 24 + cpu.mem[source_mem_addr]
    cpu.reg[target_reg_addr] = data
    cpu.pc = cpu.pc+1

def Op_ADD(cpu, op):
    target_reg_addr = op[1]
    source_reg_addr1 = op[2]
    source_reg_addr2 = op[3]
    data1 = cpu.reg[source_reg_addr1]#32list
    data2 = cpu.reg[source_reg_addr2]#32list
    result = List2Num(data1,32) + List2Num(data2,32)
    cpu.reg[target_reg_addr] = Num2List(result,32)
    cpu.pc = cpu.pc+1

def Op_SB(cpu, op):
    target_mem_addr = op[2]
    source_reg_addr = op[1]
    data = cpu.reg[source_reg_addr]#32list
    cpu.mem[target_mem_addr] = data[24:32]
    cpu.pc = cpu.pc+1

def Op_Finish(cpu):
    print("Instructions Implement Finish")
    m0 = List2Num(cpu.mem[0], cpu.mem_width)
    m1 = List2Num(cpu.mem[1], cpu.mem_width)
    m3 = List2Num(cpu.mem[3], cpu.mem_width)
    print("mem3 = mem0 + mem1 = %d = %d + %d" %(m3, m0, m1))
    cpu.pc = cpu.pc+1
def EXE(cpu, op):
    if(op[0] == 0):
        Op_Finish(cpu)
    if(op[0] == 1):
        Op_LB(cpu, op)
    if(op[0] == 2):
        Op_ADD(cpu, op)
    if(op[0] == 3):
        Op_SB(cpu, op)
def main():#complete result = data1 + data2
    #cpu has nothing
    cpu0 = cpu(32, 32, 8, 32, 0)
    cpu0.display_reg(0,4)
    cpu0.display_mem(0,4)
    #init cpu#####store data1, data2, data3 to cpu.mem
    data1 = -5
    data2 = -6
    data3 = 15
    addr0 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]#mem0
    addr1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]#mem1
    addr2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0]#mem2
    cpu0.store_mem(addr0, data1)
    cpu0.store_mem(addr1, data2)
    cpu0.store_mem(addr2, data3)
    cpu0.display_reg(0,4)
    cpu0.display_mem(0,4)
    #init inst_rom
    inst1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1]
    inst2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1]
    inst3 = [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,1,0,1,1,0,0,1,1]
    inst4 = [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1]
    inst5 = [0]*32
    inst_rom = []
    inst_rom.append(inst1)
    inst_rom.append(inst2)
    inst_rom.append(inst3)
    inst_rom.append(inst4)
    inst_rom.append(inst5)
    #print(inst_rom)
    pc0 = 0
    while(pc0 < 5):
        op = Decode(inst_rom[pc0])
        EXE(cpu0, op)
        pc0 = cpu0.pc

    '''
    op1 = Decode(inst1)
    op2 = Decode(inst2)
    op3 = Decode(inst3)
    op4 = Decode(inst4)
    op5 = Decode(inst5)
    EXE(cpu0, op1)
    EXE(cpu0, op2)
    EXE(cpu0, op3)
    EXE(cpu0, op4)
    EXE(cpu0, op5)
    '''
    cpu0.display_reg(0,4)
    cpu0.display_mem(0,4)

    num1 = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    num2 = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    #print(List2Num(num2, 32))

if __name__ == "__main__":
	main()
