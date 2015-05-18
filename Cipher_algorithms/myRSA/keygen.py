#!/usr/bin/env python
import bigNum
import simple_test
import argparse
import sys

def create_Parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-public', type=argparse.FileType(mode='wb'))
    parser.add_argument ('-private', type=argparse.FileType(mode='wb'))
    
    return parser

def ext_euclid(a, b):#calculates ax+by = gcd(a,b), return gcd,x,y
    if b == 0:
        return a, 1, 0
    if a == 0:
        return b, 1, 0

    x2 = bigNum.bigNum(1)
    x1 = bigNum.bigNum(0)
    y2 = bigNum.bigNum(0)
    y1 = bigNum.bigNum(1)

    while b > 0:
        q = a / b
        r = a - q * b
        xx = x2 - q * x1
        yy = y2 - q * y1
        a = b
        b = r
        x2 = x1
        x1 = xx
        y2 = y1
        y1 = yy

    return a, x2, y2

def keygen():
    e = bigNum.bigNum(65537)
    gcd, d = bigNum.bigNum(0), bigNum.bigNum(0)
    
    while gcd != 1:
        while d < 2:
            p = simple_test.simple_gen(100)
            q = simple_test.simple_gen(100)
            fi = (p-1) * (q-1)
            gcd, x, d = ext_euclid(fi,e)
    
    print"p and q generated"
    n = bigNum.bigNum(1)
    n = p * q
    
    return e, d, n

def main():
    e, d, n = keygen()

    parser = create_Parser()
    args = parser.parse_args(sys.argv[1:])

    args.public.write(bytes(e) + '\n' + bytes(n))
    args.private.write(bytes(d) + '\n' + bytes(n))
    

if __name__=='__main__':
    main()
