#!/usr/bin/env python3
#coding: utf8

import socket
import sys
import argparse
import viginer
import AES_128_Rijndael
import StegLSB
from PIL import Image

def create_Parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-i', '--text', type=argparse.FileType(mode='rb'))
    parser.add_argument ('-vk', '--viginerkey', type=argparse.FileType(mode='rb'))
    parser.add_argument ('-ak', '--aeskey', type=argparse.FileType(mode='rb'))
    parser.add_argument ('-im', '--image', help="image for hiding")
    parser.add_argument ('-o', '--outimg', help="container")

    return parser

if __name__ == '__main__':
    parser = create_Parser()
    args = parser.parse_args(sys.argv[1:])

    viginer_code = viginer.coding(args.text.read(), args.viginerkey.read())
    AES_code = AES_128_Rijndael.encrypt(viginer_code, args.aeskey.read())
    steg_res = StegLSB.hiding(args.image, AES_code)
    steg_res.save(args.outimg, "BMP")

    HOST = 'localhost'
    PORT = 9559
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    with open(args.outimg, 'rb') as f:
        data = f.read()
    s.send(data)
    print('Sending data...')
    s.close()
