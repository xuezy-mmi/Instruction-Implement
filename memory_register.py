#!/usr/bin/python
# -*- coding: utf-8 -*-

global memory
global register

memory = {}
register = {}


#memory单元类
class Memory_unit():

	global memory

	def __init__(self, address):
		self.address = address
		memory[self.address] = bin(0).split('b')[1].zfill(8)

	def store(self, data):
		self.data = data
		memory[self.address] = self.data

	def load(self):
		return memory[self.address]


#register单元类
class Register_unit():

	global register

	def __init__(self, address):
		self.address = address
		register[self.address] = bin(0).split('b')[1].zfill(32)

	def store(self, data):
		self.data = data
		register[self.address] = self.data

	def load(self):
		return register[self.address]


#memory和register初始化
def memory_register_initial():
	global memory_list
	global register_list

	try:
		memory_size = int(1024*float(input("Input the size of memory(kByte): ")))
	except:
		print("ERROR: please input the right size of memory!\n")
		memory_register_initial()

	if memory_size < 0:
		print("ERROR: size of memory must be greater than 0!\n")
		memory_register_initial()

	address_memory = []
	memory_list = []
	
	try:
		for address_memory_decimal in range(memory_size):
			address_memory_binary = bin(address_memory_decimal).split('b')[1].zfill(32)
			address_memory.append(address_memory_binary)

		for item in address_memory:
			memory_list.append(Memory_unit(item))

		print('Memory initial success!')
	except:
		print('Memory initial fail!')
		memory_register_initial()

	address_register = []
	register_list = []

	try:
		for address_register_decimal in range(32):
			address_register_binary = bin(address_register_decimal).split('b')[1].zfill(32)
			address_register.append(address_register_binary)

		for item in address_register:
			register_list.append(Register_unit(item))

		print('Register initial success!')
	except:
		print('Registers initial fail!')
		memory_register_initial()


#指令执行
def execute_instruction(instruction, flag_end_mode):
	global memory_list
	global register

	#Load指令
	if instruction.split(' ')[0] == 'Load':
		register_address = bin(int(instruction.split('r')[1].split(',')[0])).split('b')[1].zfill(32)
		memory_address1 = bin(int(instruction.split('#')[1])*4).split('b')[1].zfill(32)
		memory_address2 = bin(int(instruction.split('#')[1])*4+1).split('b')[1].zfill(32)
		memory_address3 = bin(int(instruction.split('#')[1])*4+2).split('b')[1].zfill(32)
		memory_address4 = bin(int(instruction.split('#')[1])*4+3).split('b')[1].zfill(32)

		for i in range(len(memory_list)):
			if memory_list[i].address == memory_address1:
				memory_unit1 = memory_list[i]
			elif memory_list[i].address == memory_address2:
				memory_unit2 = memory_list[i]
			elif memory_list[i].address == memory_address3:
				memory_unit3 = memory_list[i]
			elif memory_list[i].address == memory_address4:
				memory_unit4 = memory_list[i]

		if flag_end_mode == 'B':
			str1 = memory_unit1.load()
			str2 = memory_unit2.load()
			str3 = memory_unit3.load()
			str4 = memory_unit4.load()
			str_sum = str1 + str2 + str3 + str4

			for i in range(len(register_list)):
				if register_list[i].address == register_address:
					register_unit = register_list[i]

			register_unit.store(str_sum)

		elif flag_end_mode == 'L':
			str1 = memory_unit4.load()
			str2 = memory_unit3.load()
			str3 = memory_unit2.load()
			str4 = memory_unit1.load()
			str_sum = str1 + str2 + str3 + str4

			for i in range(len(register_list)):
				if register_list[i].address == register_address:
					register_unit = register_list[i]

			register_unit.store(str_sum)

	#Add指令
	elif instruction.split(' ')[0] == 'Add':
		result_register_address = bin(int(instruction.split('r')[1].split(',')[0])).split('b')[1].zfill(32)
		add_register_address1 = bin(int(instruction.split('r')[2].split(',')[0])).split('b')[1].zfill(32)
		add_register_address2 = bin(int(instruction.split('r')[3])).split('b')[1].zfill(32)

		for i in range(len(register_list)):
			if register_list[i].address == result_register_address:
				result_register_unit = register_list[i]
			elif register_list[i].address == add_register_address1:
				add_register_unit1 = register_list[i]
			elif register_list[i].address == add_register_address2:
				add_register_unit2 = register_list[i]
		
		result_register_unit.store(bin(int(add_register_unit1.load(), 2)+int(add_register_unit2.load(), 2)).split('b')[1].zfill(32))

	#Store指令
	elif instruction.split(' ')[0] == 'Store':
		register_address = bin(int(instruction.split('r')[2].split(',')[0])).split('b')[1].zfill(32)
		memory_address1 = bin(int(instruction.split('#')[1])*4).split('b')[1].zfill(32)
		memory_address2 = bin(int(instruction.split('#')[1])*4+1).split('b')[1].zfill(32)
		memory_address3 = bin(int(instruction.split('#')[1])*4+2).split('b')[1].zfill(32)
		memory_address4 = bin(int(instruction.split('#')[1])*4+3).split('b')[1].zfill(32)

		for i in range(len(register_list)):
				if register_list[i].address == register_address:
					register_unit = register_list[i]

		data = register_unit.load()

		for i in range(len(memory_list)):
			if memory_list[i].address == memory_address1:
				memory_unit1 = memory_list[i]
			elif memory_list[i].address == memory_address2:
				memory_unit2 = memory_list[i]
			elif memory_list[i].address == memory_address3:
				memory_unit3 = memory_list[i]
			elif memory_list[i].address == memory_address4:
				memory_unit4 = memory_list[i]

		if flag_end_mode == 'B':
			memory_unit1.store(data[:8])
			memory_unit2.store(data[8:16])
			memory_unit3.store(data[16:24])
			memory_unit4.store(data[24:32])
		elif flag_end_mode == 'L':
			memory_unit4.store(data[:8])
			memory_unit3.store(data[8:16])
			memory_unit2.store(data[16:24])
			memory_unit1.store(data[24:32])

	#自定义Store_num指令
	elif instruction.split(' ')[0] == 'Store_num':
		data = bin(int(instruction.split(' ')[1])).split('b')[1].zfill(32)
		memory_address1 = bin(int(instruction.split('#')[1])*4).split('b')[1].zfill(32)
		memory_address2 = bin(int(instruction.split('#')[1])*4+1).split('b')[1].zfill(32)
		memory_address3 = bin(int(instruction.split('#')[1])*4+2).split('b')[1].zfill(32)
		memory_address4 = bin(int(instruction.split('#')[1])*4+3).split('b')[1].zfill(32)

		for i in range(len(memory_list)):
			if memory_list[i].address == memory_address1:
				memory_unit1 = memory_list[i]
			elif memory_list[i].address == memory_address2:
				memory_unit2 = memory_list[i]
			elif memory_list[i].address == memory_address3:
				memory_unit3 = memory_list[i]
			elif memory_list[i].address == memory_address4:
				memory_unit4 = memory_list[i]

		if flag_end_mode == 'B':
			memory_unit1.store(data[:8])
			memory_unit2.store(data[8:16])
			memory_unit3.store(data[16:24])
			memory_unit4.store(data[24:32])
		elif flag_end_mode == 'L':
			memory_unit4.store(data[:8])
			memory_unit3.store(data[8:16])
			memory_unit2.store(data[16:24])
			memory_unit1.store(data[24:32])

	#自定义Print_memory指令
	elif instruction.split(' ')[0] == 'Print_memory':
		memory_address1 = bin(int(instruction.split('#')[1])*4).split('b')[1].zfill(32)
		memory_address2 = bin(int(instruction.split('#')[1])*4+1).split('b')[1].zfill(32)
		memory_address3 = bin(int(instruction.split('#')[1])*4+2).split('b')[1].zfill(32)
		memory_address4 = bin(int(instruction.split('#')[1])*4+3).split('b')[1].zfill(32)

		for i in range(len(memory_list)):
			if memory_list[i].address == memory_address1:
				memory_unit1 = memory_list[i]
			elif memory_list[i].address == memory_address2:
				memory_unit2 = memory_list[i]
			elif memory_list[i].address == memory_address3:
				memory_unit3 = memory_list[i]
			elif memory_list[i].address == memory_address4:
				memory_unit4 = memory_list[i]

		if flag_end_mode == 'B':
			str1 = memory_unit1.load()
			str2 = memory_unit2.load()
			str3 = memory_unit3.load()
			str4 = memory_unit4.load()
			print(str1 + str2 + str3 + str4)
			return str1 + str2 + str3 + str4
		elif flag_end_mode == 'L':
			str1 = memory_unit4.load()
			str2 = memory_unit3.load()
			str3 = memory_unit2.load()
			str4 = memory_unit1.load()
			print(str1 + str2 + str3 + str4)
			return str1 + str2 + str3 + str4

	#自定义Print_register指令
	elif instruction.split(' ')[0] == 'Print_register':
		register_address = bin(int(instruction.split('r')[-1])).split('b')[1].zfill(32)

		for i in range(len(register_list)):
				if register_list[i].address == register_address:
					register_unit = register_list[i]

		print(register_unit.load())


def main():
	#B为大端模式，L为小端模式
	flag_end_mode = input("Input big end mode or small end mode(B/L): ")
	if flag_end_mode == 'B' or flag_end_mode == 'L':
		pass
	else:
		print("ERROR: please input the right end mode!\n")
		main()

	#自定义指令
	add_num1 = int(input('Please input num1: '))
	add_num2 = int(input('Please input num2: '))
	execute_instruction('Store_num '+str(add_num1)+' #0', flag_end_mode)
	execute_instruction('Store_num '+str(add_num2)+' #1', flag_end_mode)
	print('Value of #0 memory is ', end='')
	execute_instruction('Print_memory #0', flag_end_mode)
	print('Value of #1 memory is ', end='')
	execute_instruction('Print_memory #1', flag_end_mode)

	#设计实现的指令
	execute_instruction('Load r1,#0', flag_end_mode)
	execute_instruction('Load r2,#1', flag_end_mode)
	print('Value of r1 register is ', end='')
	execute_instruction('Print_register r1', flag_end_mode)
	print('Value of r2 register is ', end='')
	execute_instruction('Print_register r2', flag_end_mode)
	execute_instruction('Add r3,r1,r2', flag_end_mode)
	print('Value of r3 register is ', end='')
	execute_instruction('Print_register r3', flag_end_mode)
	execute_instruction('Store r3,#3', flag_end_mode)

	#自定义指令
	print('Value of #3 memory is ', end='')
	result = int(execute_instruction('Print_memory #3', flag_end_mode), 2)
	print(str(add_num1)+'和'+str(add_num2)+'相加结果为： ', result)

	
if __name__ == "__main__":
	memory_register_initial()
	main()