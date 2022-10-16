#!/usr/bin/python
# -*- coding: utf-8 -*-

def data_to_complement(num):
	if num >= 0:
		#补码
		complement = bin(num).split('b')[1].zfill(32)
	else:
		num = -num
		#原码
		source = 'One' + bin(num).split('b')[1].zfill(31)
		#反码
		inverse = source.replace('1', 'z').replace('0', '1').replace('z', '0').replace('One', '1')
		#补码
		complement = '1' + bin(int(inverse[1:], 2)+1).split('b')[1].zfill(31)
		
	return complement

def complement_to_data(complement):
	if complement[0] == '1':
		#反码
		num = int(complement[1:], 2) - 1
		inverse = '1' + bin(num).split('b')[1].zfill(31)
		#原码
		source = '1' + inverse[1:].replace('1', 'z').replace('0', '1').replace('z', '0')

		data = -int(source[1:], 2)
	else:
		data = int(complement, 2)
	
	return data


def main():
	print(len(data_to_complement(1)))
	print(data_to_complement(-1))

	print(complement_to_data('00000000000000000000000000000001'))
	print(complement_to_data('11111111111111111111111111111111'))


if __name__ == "__main__":
	main()