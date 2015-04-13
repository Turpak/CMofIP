#!/usr/bin/env python3
import math
import sys
import argparse

def create_Parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-i', '--input', type=argparse.FileType(mode='rb'))
    parser.add_argument ('-o', '--output', type=argparse.FileType(mode='w'))

    return parser
 
def left_rotate(x, s):
    x &= 0xffffffff
    return ((x<<s) | (x>>(32-s))) & 0xffffffff
 
def md5(message):
     
    rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                  5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

    constants = [int(abs(math.sin(i+1)) * 2**32) & 0xffffffff for i in range(64)]

    init_abcd = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

    functions = 16*[lambda x, y, z: (x & y) | (~x & z)] + \
            16*[lambda x, y, z: (z & x) | (~z & y)] + \
            16*[lambda x, y, z: x ^ y ^ z] + \
            16*[lambda x, y, z: y ^ (x | ~z)]
 
    index_functions = 16*[lambda i: i] + \
                  16*[lambda i: (5*i + 1)%16] + \
                  16*[lambda i: (3*i + 5)%16] + \
                  16*[lambda i: (7*i)%16] 
    message = bytearray(message)
    
    orig_len_in_bits = (8 * len(message)) & 0xffffffffffffffff
    
    message.append(0x80)
    
    while len(message)%64 != 56:
        message.append(0)
    
    message += orig_len_in_bits.to_bytes(8, byteorder='little')
 
    hash_pieces = init_abcd[:]
 
    for chunk_ofst in range(0, len(message), 64):
        a, b, c, d = hash_pieces
        chunk = message[chunk_ofst:chunk_ofst+64]
        for i in range(64):
            f = functions[i](b, c, d)
            g = index_functions[i](i)
            to_rotate = a + f + constants[i] + int.from_bytes(chunk[4*g:4*g+4], byteorder='little')
            new_b = (b + left_rotate(to_rotate, rotate_amounts[i])) & 0xffffffff
            a, b, c, d = d, new_b, b, c
        for i, val in enumerate([a, b, c, d]):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xffffffff

    return sum(x*(0x100000000**i) for i, x in enumerate(hash_pieces))
     
 
def hash_in_hex(bufferABCD):
    tmp = bufferABCD.to_bytes(16, byteorder='little')

    return '{:032x}'.format(int.from_bytes(tmp, byteorder='big'))

def main ():
    parser = create_Parser()
    arguments = parser.parse_args(sys.argv[1:])

    final = hash_in_hex(md5(arguments.input.read()))
    arguments.output.write(final)
 
if __name__=='__main__':
    main()
