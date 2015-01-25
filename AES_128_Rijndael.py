#!/usr/bin/env python3

import sys
import argparse

def create_Parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-i', '--input', type=argparse.FileType(mode='rb'))
    parser.add_argument ('-k', '--key', type=argparse.FileType(mode='rb'))
    parser.add_argument ('-o', '--output', type=argparse.FileType(mode='wb'))
    parser.add_argument ('-cod', choices=['c', 'd'], default='c')

    return parser

def coding(indata, key):
    mid_result = [[] for i in range(4)]
    for r in range(4):
        for c in range(num_of_col):
            mid_result[r].append(indata[r + 4 * c])

    num_rnd = 0
    value = 0
    key_round = key_transform(key)
    mid_result = xor_transform(mid_result, key_round, num_rnd)

    for num_rnd in range(1, num_of_rnd):
        mid_result = replacing(mid_result, value)
        mid_result = moving(mid_result, value)
        mid_result = multing(mid_result, value)
        mid_result = xor_transform(mid_result, key_round, num_rnd)

    mid_result = replacing(mid_result, value)
    mid_result = moving(mid_result, value)
    mid_result = xor_transform(mid_result, key_round, num_rnd + 1)

    outdata = [[] for i in range(num_of_col * 4)]
    for r in range(4):
        for c in range(num_of_col):
            outdata[r + 4 * c] = mid_result[r][c]

    return outdata

def replacing(mid_res, val):
    if val == 0:
        table = const_table
    else:
        table = inv_const_table

    hex_ten = 0x10
    for i in range(len(mid_res)):
        for j in range(len(mid_res[i])):
            line = mid_res[i][j] // hex_ten
            column = mid_res[i][j] % hex_ten
            tmp = table[16 * line + column]
            mid_res[i][j] = tmp

    return mid_res

def left_move(arr, row):
    outarr = arr[:]

    for i in range(row):
        tmp = outarr[1:]
        tmp.append(outarr[0])
        outarr[:] = tmp[:]

    return outarr

def right_move(arr, row):
    outarr = arr[:]

    for i in range(row):
        tmp = outarr[:-1]
        tmp.insert(0, outarr[-1])
        outarr[:] = tmp[:]

    return outarr

def moving(mid_res, val):
    row = 1

    if val == 0:
        for j in range(1, num_of_col):
            mid_res[j] = left_move(mid_res[j], row)
            row = row + 1
    else:
        for j in range(1, num_of_col):
            mid_res[j] = right_move(mid_res[j], row)
            row = row + 1

    return mid_res

def mulhex_02(amount):
    if amount < 0x80:
        outres = (amount << 1)
    else:
        outres = (amount << 1) ^ 0x1b

    outres = outres % 0x100

    return outres

def mulhex_03(amount):
    outres = mulhex_02(amount) ^ amount

    return outres

def mulhex_09(amount):
    outres = mulhex_02(mulhex_02(mulhex_02(amount))) ^ amount

    return outres

def mulhex_0b(amount):
    outres = mulhex_02(mulhex_02(mulhex_02(amount))) ^ mulhex_02(amount) ^ amount

    return outres

def mulhex_0d(amount):
    outres = mulhex_02(mulhex_02(mulhex_02(amount))) ^ mulhex_02(mulhex_02(amount)) ^ amount

    return outres

def mulhex_0e(amount):
    outres = mulhex_02(mulhex_02(mulhex_02(amount))) ^ mulhex_02(mulhex_02(amount)) ^ mulhex_02(amount)

    return outres

def multing(mid_result, val):
    if val == 0:
        for i in range(num_of_col):
            tmp0 = mulhex_02(mid_result[0][i]) ^ mulhex_03(mid_result[1][i]) ^ mid_result[2][i] ^ mid_result[3][i]
            tmp1 = mid_result[0][i] ^ mulhex_02(mid_result[1][i]) ^ mulhex_03(mid_result[2][i]) ^ mid_result[3][i]
            tmp2 = mid_result[0][i] ^ mid_result[1][i] ^ mulhex_02(mid_result[2][i]) ^ mulhex_03(mid_result[3][i])
            tmp3 = mulhex_03(mid_result[0][i]) ^ mid_result[1][i] ^ mid_result[2][i] ^ mulhex_02(mid_result[3][i])

            mid_result[0][i] = tmp0
            mid_result[1][i] = tmp1
            mid_result[2][i] = tmp2
            mid_result[3][i] = tmp3
    else:
        for j in range(num_of_col):
            tmp0 = mulhex_0e(mid_result[0][j]) ^ mulhex_0b(mid_result[1][j]) ^ mulhex_0d(mid_result[2][j]) ^ mulhex_09(mid_result[3][j])
            tmp1 = mulhex_09(mid_result[0][j]) ^ mulhex_0e(mid_result[1][j]) ^ mulhex_0b(mid_result[2][j]) ^ mulhex_0d(mid_result[3][j])
            tmp2 = mulhex_0d(mid_result[0][j]) ^ mulhex_09(mid_result[1][j]) ^ mulhex_0e(mid_result[2][j]) ^ mulhex_0b(mid_result[3][j])
            tmp3 = mulhex_0b(mid_result[0][j]) ^ mulhex_0d(mid_result[1][j]) ^ mulhex_09(mid_result[2][j]) ^ mulhex_0e(mid_result[3][j])

            mid_result[0][j] = tmp0
            mid_result[1][j] = tmp1
            mid_result[2][j] = tmp2
            mid_result[3][j] = tmp3

    return mid_result

def key_transform(key):
    if len(key) < 16:
        k = []
        for i in range(len(key)):
            k.append(key[i])
        for i in range(16 - len(key)):
             k.append(0x01)
        key = k
            

            
    round_key = [[] for i in range(4)]
    for r in range(4):
        for c in range(len_of_key):
            round_key[r].append(key[r + 4 * c])

    for col in range(len_of_key, num_of_col * (num_of_rnd + 1)):
        if col % len_of_key == 0:
            iter_key = [round_key[line][col - 1] for line in range(1,4)]
            iter_key.append(round_key[0][col - 1])

            for j in range(len(iter_key)):
                r = iter_key[j] // 0x10
                c = iter_key[j] % 0x10
                temp = const_table[16 * r + c]
                iter_key[j] = temp

            for r in range(4):
                xor_c = (round_key[r][col - 4]) ^ (iter_key[r]) ^ (table_for_key[r][int(col / len_of_key - 1)])
                round_key[r].append(xor_c)

        else:
            for r in range(4):
                xor_c = (round_key[r][col - 4]) ^ (round_key[r][col - 1])
                round_key[r].append(xor_c)

    return round_key

def xor_transform(mid_result, key_round, num_rnd):
    for col in range(len_of_key):
        tmp0 = mid_result[0][col] ^ key_round[0][num_of_col * num_rnd + col]
        tmp1 = mid_result[1][col] ^ key_round[1][num_of_col * num_rnd + col]
        tmp2 = mid_result[2][col] ^ key_round[2][num_of_col * num_rnd + col]
        tmp3 = mid_result[3][col] ^ key_round[3][num_of_col * num_rnd + col]

        mid_result[0][col] = tmp0
        mid_result[1][col] = tmp1
        mid_result[2][col] = tmp2
        mid_result[3][col] = tmp3

    return mid_result

def decoding(indata, key):
    mid_result = [[] for i in range(4)]
    for r in range(4):
        for c in range(num_of_col):
            mid_result[r].append(indata[r + 4 * c])

    num_rnd = num_of_rnd
    value = 1
    key_round = key_transform(key)
    mid_result = xor_transform(mid_result, key_round, num_rnd)

    for num_rnd in range(num_of_rnd - 1, 0, -1): 
        mid_result = moving(mid_result, value)
        mid_result = replacing(mid_result, value)
        mid_result = xor_transform(mid_result, key_round, num_rnd)
        mid_result = multing(mid_result, value)
        
    num_rnd = 0
    mid_result = moving(mid_result, value)
    mid_result = replacing(mid_result, value)
    mid_result = xor_transform(mid_result, key_round, num_rnd)

    outdata = [[] for i in range(num_of_col * 4)]
    for r in range(4):
        for c in range(num_of_col):
            outdata[r + 4 * c] = mid_result[r][c]

    return outdata

def encrypt (filein, arguments):
     final_result = []
     data = []
     for byte in filein:
         data.append(byte)
         if len(data) == 16:
             block = coding(data, arguments.key.read())
             final_result.extend(block)
             del data[:]
     else:
         if 0 < len(data) < 16:
             free_pos = 16 - len(data)
             for i in range(free_pos - 1):
                 data.append(0)
             data.append(1)
             block = coding(data, arguments.key.read())
             final_result.extend(block)
     arguments.output.write(bytes(final_result))
     
     print('AES coding has successfully done!')

def decrypt (filein, arguments):
    final_result = []
    data = []
    for byte in filein:
        data.append(byte)
        if len(data) == 16:
            block = decoding(data, arguments.key.read())
            final_result.extend(block)
            del data[:]
    else:
        if 0 < len(data) < 16:
            free_pos = 16 - len(data)
            for i in range(free_pos - 1):
                data.append(0)
            data.append(1)
            block = decoding(data, arguments.key.read())
            final_result.extend(block)
    arguments.output.write(bytes(final_result))
    print('AES decoding has successfully done!')

if __name__ == '__main__':
    parser = create_Parser()
    arguments = parser.parse_args(sys.argv[1:])
    code = 'c'
    decode = 'd'
    num_of_col = 4
    num_of_rnd = 10
    len_of_key = 4
    const_table = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
        ]
    inv_const_table = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
        ]
    table_for_key = [
        [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36],
        [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        ]

        
    if arguments.cod == code:
        encrypt(arguments.input.read(), arguments)
    else:
        decrypt(arguments.input.read(), arguments)
