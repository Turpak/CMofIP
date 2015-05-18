#!/usr/bin/env python
import bigNum
import simple_test
import argparse
import sys

def create_Parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-action', choices=['e','d'], help ='encrypt or decrypt')
    parser.add_argument ('-i', '--input', type=argparse.FileType(mode='rb'))
    parser.add_argument ('-o', '--output')
    parser.add_argument ('-pub', '--public', type=argparse.FileType(mode='rb'))
    parser.add_argument ('-priv', '--private', type=argparse.FileType(mode='rb'))
        
    return parser

def encrypt(m,e,n):
    if m >= n:
        raise ValueError('Please, remember that m < n! :)')
        
    c = bigNum.to_pow(m,e,n)

    return c

def decrypt(c,d,n):
    m = bigNum.to_pow(c,d,n)

    return m

def main():
    parser = create_Parser()
    args = parser.parse_args(sys.argv[1:])

    if args.action == 'e':
        msg = args.input.read()
        ee = args.public.readline() 
        nn = args.public.readline()
    
        m = bigNum.bigNum(msg[3:])
        e = bigNum.bigNum(ee[:len(ee)-1])
        n = bigNum.bigNum(nn)

        c = encrypt(m,e,n)

        with open(args.output, 'wb') as f:
            f.write(bytes(c))

        print"RSA encrypt is done!"
     
    elif args.action == 'd':
        with open(args.output, 'rb') as f:
            msg = f.read()
        
        dd = args.private.readline() 
        nn = args.private.readline()

        c = bigNum.bigNum(msg)
        d = bigNum.bigNum(dd[:len(dd)-1])
        n = bigNum.bigNum(nn)

        m = decrypt(c,d,n)

        print"m =",m
        print"\nRSA decrypt is done!"
            
if __name__=='__main__':
    main()
