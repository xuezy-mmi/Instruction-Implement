#!/usr/bin/python
# -*- coding: utf-8 -*-

from data_trans import *

#memory unit class
class Memory_unit():
	def __init__(self, address):
		self.address = address
		self.data = bin(0).split('b')[1].zfill(8)

	def store(self, data):
		self.data = data

	def load(self):
		return self.data

	def show(self):
		print('memory-->', self.address, ':', self.data)

#register unit calss
class Register_unit():
	def __init__(self, address):
		self.address = address
		self.data = bin(0).split('b')[1].zfill(32)

	def store(self, data):
		self.data = data

	def load(self):
		return self.data

	def show(self):
		print('register-->', self.address, ':', self.data)


#memory register initial
def memory_register_initial():
	global memory
	global register
	global flag_end_mode

	#B--Big end model  L--Little end model
	flag_end_mode = input("Input big end mode or small end mode(B/L): ")
	if flag_end_mode == 'B' or flag_end_mode == 'L':
		pass
	else:
		print("ERROR: please input the right end mode!\n")
		memory_register_initial()

	try:
		memory_size = int(1024*float(input("Input the size of memory(kByte): ")))
	except:
		print("ERROR: please input the right size of memory!\n")
		memory_register_initial()

	if memory_size < 0:
		print("ERROR: size of memory must be greater than 0!\n")
		memory_register_initial()

	address_memory = []
	memory = {}
	
	try:
		for address_memory_decimal in range(memory_size):
			address_memory_hexadecimal = '0x'+hex(address_memory_decimal).split('x')[1].zfill(8)
			address_memory.append(address_memory_hexadecimal)

		for address in address_memory:
			memory[address] = Memory_unit(address)

		print('Memory initial success!')
	except:
		print('Memory initial fail!')
		memory_register_initial()

	address_register = []
	register = {}

	try:
		for address_register_decimal in range(32):
			address_register_hexadecimal = '0x'+hex(address_register_decimal).split('x')[1].zfill(8)
			address_register.append(address_register_hexadecimal)

		for address in address_register:
			register[address] = Register_unit(address)

		print('Register initial success!')
	except:
		print('Registers initial fail!')
		memory_register_initial()


#read 4 byte data from memory once
def read_memory_4byte(address):
	if flag_end_mode == 'B':
		data1 = memory['0x'+hex(int(address)).split('x')[1].zfill(8)].load()
		data2 = memory['0x'+hex(int(address)+1).split('x')[1].zfill(8)].load()
		data3 = memory['0x'+hex(int(address)+2).split('x')[1].zfill(8)].load()
		data4 = memory['0x'+hex(int(address)+3).split('x')[1].zfill(8)].load()
		data = data1 + data2 + data3 + data4
	elif flag_end_mode == 'L':
		data1 = memory['0x'+hex(int(address)+3).split('x')[1].zfill(8)].load()
		data2 = memory['0x'+hex(int(address)+2).split('x')[1].zfill(8)].load()
		data3 = memory['0x'+hex(int(address)+1).split('x')[1].zfill(8)].load()
		data4 = memory['0x'+hex(int(address)).split('x')[1].zfill(8)].load()
		data = data1 + data2 + data3 + data4

	return data
	

#write 4 byte data to memory once
def write_memory_4byte(address, data):
	data = data_to_complement(data)

	if flag_end_mode == 'B':
		memory['0x'+hex(int(address)).split('x')[1].zfill(8)].store(data[:8])
		memory['0x'+hex(int(address)+1).split('x')[1].zfill(8)].store(data[8:16])
		memory['0x'+hex(int(address)+2).split('x')[1].zfill(8)].store(data[16:24])
		memory['0x'+hex(int(address)+3).split('x')[1].zfill(8)].store(data[24:32])
	elif flag_end_mode == 'L':
		memory['0x'+hex(int(address)+3).split('x')[1].zfill(8)].store(data[:8])
		memory['0x'+hex(int(address)+2).split('x')[1].zfill(8)].store(data[8:16])
		memory['0x'+hex(int(address)+1).split('x')[1].zfill(8)].store(data[16:24])
		memory['0x'+hex(int(address)).split('x')[1].zfill(8)].store(data[24:32])
		

#read 4 byte data from register once
def read_register_4byte(address):
	return register['0x'+hex(int(address)).split('x')[1].zfill(8)].load()


#write 4 byte data to memory once
def write_register_4byte(address, data):
	data = data_to_complement(data)
	register['0x'+hex(int(address)).split('x')[1].zfill(8)].store(data)