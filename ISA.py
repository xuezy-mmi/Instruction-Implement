#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
汇编指令：
LOADI $1 #0x1      0x0c200004
LOADI $2 #0x2      0x0c400008
ADD $0 $1 $2      0x00011020
STOREI $0 #0x0     0x04000000

R型指令：op--000000
ADDU $0 $1 $2: 000000 00000 00001 00010 00000 100001    0x00011021

I型指令：op--000011 or 000001
LOADI $1 #0x4: 000011 00001 00000 00000 00000 000100    0x0c200004
LOADI $2 #0x8: 000011 00010 00000 00000 00000 001000    0x0c400008
STOREI $0 #0x0: 000001 00000 00000 00000 00000 000000   0x04000000
'''

import time
from data_trans import *
from memory_register import *

class Instruction():
	def __init__(self, instruction):
		self.instruction = instruction
		self.opcode = int(self.instruction, 2) >> 26
		if self.opcode == int('0b000000', 2): #R type
			self.type = 'R'
			self.rs = int(self.instruction, 2) >> 21 & 0x1f
			self.rt = int(self.instruction, 2) >> 16 & 0x1f
			self.rd = int(self.instruction, 2) >> 11 & 0x1f
			self.shamt = int(self.instruction, 2) >> 6 & 0x1f
			self.func = int(self.instruction, 2) & 0x3f
		elif self.opcode == int('0b000010', 2): #J type
			self.type = 'J'
			self.address = int(self.instruction, 2) & 0x3ffffff
		elif self.opcode == int('0b000011', 2) or self.opcode == int('0b000001', 2): #I type
			self.type = 'I'
			self.rs = int(self.instruction, 2) >> 21 & 0x1f
			self.rt = int(self.instruction, 2) >> 16 & 0x1f
			self.immediate = int(self.instruction, 2) & 0xffff

	def execute(self):
		'''
		write_memory_4byte(0x1000, 0x80000fff)
		print(read_memory_4byte(0x1000))
		write_register_4byte(0x000f, 0x80000fff)
		print(read_register_4byte(0x000f))
		'''
		if self.type == 'R':
			if self.func == int('0b100001', 2): #ADDU $0 $1 $2
				rt_result = read_register_4byte(self.rt)
				rd_result = read_register_4byte(self.rd)
				add_num = int('0b'+rt_result, 2) + int('0b'+rd_result, 2)
				write_register_4byte(self.rs, add_num)
			elif self.func == int('0b100000', 2): #ADD $0 $1 $2
				rt_result = read_register_4byte(self.rt)
				rd_result = read_register_4byte(self.rd)
				rt_result = complement_to_data(rt_result)
				rd_result = complement_to_data(rd_result)
				add_num = rt_result + rd_result
				write_register_4byte(self.rs, add_num)
			elif self.func == int('0b100010', 2): #SUB $0 $1 $2
				rt_result = read_register_4byte(self.rt)
				rd_result = read_register_4byte(self.rd)
				rt_result = complement_to_data(rt_result)
				rd_result = complement_to_data(rd_result)
				sub_num = rt_result - rd_result
				write_register_4byte(self.rs, sub_num)
			elif self.func == int('0b100011', 2): #SUBU $0 $1 $2
				rt_result = read_register_4byte(self.rt)
				rd_result = read_register_4byte(self.rd)
				sub_num = int('0b'+rt_result, 2) - int('0b'+rd_result, 2)
				write_register_4byte(self.rs, sub_num)
			elif self.func == int('0b100100', 2): #AND $0 $1 $2
				rt_result = read_register_4byte(self.rt)
				rd_result = read_register_4byte(self.rd)
				rt_result = complement_to_data(rt_result)
				rd_result = complement_to_data(rd_result)
				and_num = rt_result & rd_result
				write_register_4byte(self.rs, sub_num)
			elif self.func == int('0b100101', 2): #OR $0 $1 $2
				rt_result = read_register_4byte(self.rt)
				rd_result = read_register_4byte(self.rd)
				rt_result = complement_to_data(rt_result)
				rd_result = complement_to_data(rd_result)
				or_num = rt_result | rd_result
				write_register_4byte(self.rs, or_num)
			elif self.func == int('0b100110', 2): #XOR $0 $1 $2
				rt_result = read_register_4byte(self.rt)
				rd_result = read_register_4byte(self.rd)
				rt_result = complement_to_data(rt_result)
				rd_result = complement_to_data(rd_result)
				xor_num = rt_result ^ rd_result
				write_register_4byte(self.rs, xor_num)
			else:
				print("R type not completed!")

		elif self.type == 'J':
			print("J type not completed!")
		else:
			if self.opcode == int('0b000011', 2): #LOADI $1 0x4
				num = int(read_memory_4byte(self.immediate), 2)
				write_register_4byte(self.rs, num)
			elif self.opcode == int('0b000001', 2): #STOREI $0 0x0
				num = int(read_register_4byte(self.rs), 2)
				write_memory_4byte(self.immediate, num)
			else:
				print("I type not completed!")


#pc extract issn from memory and execute
def Execution(start_insn_address, insn_num):
	end_insn_address = start_insn_address + (insn_num-1) * 4
	pc = start_insn_address
	while pc <= end_insn_address:
		insn = bin(eval('0b'+read_memory_4byte(pc)))
		insn_calss = Instruction(insn)
		insn_calss.execute()
		time.sleep(1)
		pc += 4


#write insn to memory
def write_insn_memory(insn_list, start_insn_address):
	start_insn_address = '0x'+hex(int(start_insn_address)).split('x')[1].zfill(8)
	for i in range(len(insn_list)):
		insn = insn_list[i]
		write_memory_4byte(eval(start_insn_address)+i*4, insn)


def main():
	memory_register_initial()

	#write data to memory here-------->
	write_memory_4byte(0x00000004, 123)
	write_memory_4byte(0x00000008, 456)
	write_memory_4byte(0x0000000c, -123)
	write_memory_4byte(0x00000010, -456)

	#for key in memory_register.memory.keys():
	#	memory_register.memory[key].show()

	#write insn to memory here-------->
	insn_list = [0x0c200004, 0x0c400008, 0x00011021, 0x04000000]
	start_insn_address = 0x00000018
	write_insn_memory(insn_list, start_insn_address)

	Execution(start_insn_address, len(insn_list))

	print('Value of #0 memory is: ', int(read_memory_4byte(0x00000000), 2))

	#for key in memory_register.register.keys():
	#	memory_register.register[key].show()
	



if __name__ == "__main__":
	main()


