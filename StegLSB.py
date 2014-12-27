#!/usr/bin/env python3
# coding: utf8

import sys
import argparse
from PIL import Image

def create_Parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-i', '--input', help="image for hiding")
    parser.add_argument ('-o', '--output', help="container with hiding mail")
    parser.add_argument ('-d', '--data', type=argparse.FileType(mode='rb'),
                         help="data-file if you want to hide information")
        
    return parser

def makebit(inbyte, param):
    y = bytearray(param)
    bi = 0b00000011
    a = bytearray()
    for i in range(param):
        y[i] = (inbyte >> 2*i) & bi
        a.append(y[i])

    return a

def hiding(picname, data):
    img = Image.open(picname)
    value = bytearray(img.tobytes())
    print (len(value))
    print (len(data))
    if len(data) > len(value) / 4 + 12:
         raise Exception('This image is not enough \
                            to hide this data, try larger image')
    size = len(data)
    arrbit = [[] for i in range(len(data))]
     
    for i in range(len(data)):
        arrbit[i] = makebit(data[i], 4)
    
    for i in range(len(data)):
        value[i] = value[i] & 0b11111100
        
    datasize = makebit(size, 12)
    print(datasize)
    
    for i in range(12):
        value[11-i] = value[11-i] | datasize[i]

    j = 12
    for i in range(len(data)):
        value[j+3] = value[j+3] | arrbit[i][0]
        value[j+2] = value[j+2] | arrbit[i][1]
        value[j+1] = value[j+1] | arrbit[i][2]
        value[j] = value[j] | arrbit[i][3]
        j = j + 4
        
    outimg = Image.frombytes(img.mode, img.size, bytes(value))
        
    return outimg


def extract(picname):
    img = Image.open(picname)
    val = bytearray(img.tobytes())

    for i in range(12):
       val[i] = val[i] & 0b00000011

    arr = [[] for i in range(3)]            
    j = 0
    for i in range(3):
        arr[i] = (val[j] << 6) + (val[j+1] << 4) + (val[j+2] << 2) + val[j+3]
        j = j + 4

    size = arr[0] * (2 ** 16) + arr[1] * (2 ** 8) + arr[2]
    #data = [[] for i in range(size)]
    data = bytearray()

    for i in range(12, size):
        val[i] = val[i] & 0b00000011
        
    for j in range(12, size, 4):
        symb = 0
        symb = (val[j] << 6) + (val[j+1] << 4) + (val[j+2] << 2) + val[j+3]
        data.append(symb)
        
    return data        
    

if __name__ == '__main__':
    parser = create_Parser()
    args = parser.parse_args(sys.argv[1:])

    if args.data:
        result = hiding(args.input, args.data.read())
        result.save(args.output, "BMP")
    else:
        result = extract(args.input)
        with open(args.output, 'wb') as file:
            file.write(result)
