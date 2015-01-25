#!/usr/bin/env python3
# coding: utf8

import socket
import sys
import argparse
import viginer
import AES_128_Rijndael
import StegLSB

def create_Parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-vk', '--viginerkey', type=argparse.FileType(mode='rb'))
    parser.add_argument ('-ak', '--aeskey', type=argparse.FileType(mode='rb'))
    parser.add_argument ('-o', '--output', type=argparse.FileType(mode='wb'))
    parser.add_argument ('-im', '--image', help="image for extract")
    
    return parser

def getmsg ():
    HOST = ''
    PORT = 9559
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()

    print('Connection is started...')
    msg = bytes()
    tmp = conn.recv(1024)
    while tmp:
        msg = msg + tmp
        tmp = conn.recv(1024)

    conn.close()
    print('Connection is broken.')
    s.close()
    
    return msg

if __name__ == '__main__':
    parser = create_Parser()
    args = parser.parse_args(sys.argv[1:])

    img = getmsg()
    with open(args.image, 'wb') as file:
        file.write(bytearray(img))
    from_img = StegLSB.extract(args.image)
    decode_AES = AES_128_Rijndael.decrypt(from_img, args.aeskey.read())
    viginer_res = viginer.decoding(decode_AES, args.viginerkey.read())
    args.output.write(viginer_res)
    print('Success! Text has been decrypted and written in file.')
