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

def coding(filein, key):
    key_length = len(key)

    return bytearray([filein[i] + key[i % key_length] % 256
                      for i in range(len(filein))])    

def decoding(filein, key):
    key_len = len(key)

    return bytearray([(filein[i] - key[i % key_len] + 256) % 256
                      for i in range(len(filein))])


if __name__ == '__main__':
    parser = create_Parser()
    arguments = parser.parse_args(sys.argv[1:])
    code = 'c'
    decode = 'd'
    if arguments.cod == code:
        result = coding(arguments.input.read(), arguments.key.read())
        arguments.output.write(result)
        print('Viginer coding has successfully done!')
    else:
        result = decoding(arguments.input.read(), arguments.key.read())
        arguments.output.write(result)
        print('Viginer decoding has successfully done!')
    
