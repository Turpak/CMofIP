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

def encrypt(M,p,g,y):
    if M >= p:
        raise ValueError('Please, remember that M < p! :)')
        
    k = bigNum.random_big(p-1)
    a = bigNum.to_pow(g,k,p)
    b = bigNum.to_pow(y,k,p)
    b = (b * M) % p

    return a,b

def decrypt(a,b,x,p):
    M = bigNum.to_pow(a,p-1-x,p)
    M = (M * b) % p

    return M

def main():
    parser = create_Parser()
    args = parser.parse_args(sys.argv[1:])

    if args.action == 'e':
        msg = args.input.read()
        pp = args.public.readline() 
        gg = args.public.readline()
        yy = args.public.readline()
    
        M = bigNum.bigNum(msg[3:])
        p = bigNum.bigNum(pp[:len(pp)-1])
        g = bigNum.bigNum(gg[:len(gg)-1])
        y = bigNum.bigNum(yy)
        print"M=",M
        print"p=",p
        print"g=",g
        print"y=",y

        a, b = encrypt(M,p,g,y)

        with open(args.output, 'wb') as f:
            f.write(bytes(a)+'\n'+bytes(b))

        print"EL_GAMAL encrypt is done!"
     
    elif args.action == 'd':
        with open(args.output, 'rb') as f:
            aa = f.readline()
            bb = f.readline()
        
        xx = args.private.readline() 
        pp = args.private.readline()

        a = bigNum.bigNum(aa[:len(aa)-1])
        b = bigNum.bigNum(bb)
        x = bigNum.bigNum(xx[:len(xx)-1])
        p = bigNum.bigNum(pp)

        M = decrypt(a,b,x,p)

        print"M =",M
        print"\nELGAMAL decrypt is done!"
            
if __name__=='__main__':
    main()
