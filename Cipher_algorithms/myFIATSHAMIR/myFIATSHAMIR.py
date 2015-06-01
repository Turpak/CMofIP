#!/usr/bin/env python
import bigNum
import simple_test
import argparse
import sys
import random

def create_Parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-s', '--secret')
        
    return parser

def pre_stage(Xfile):
    p = simple_test.simple_gen(33)
    print"p is generated..."
    q = simple_test.simple_gen(33)
    print"q is generated..."
    n = bigNum.bigNum(1)
    n = p * q
    print"n is generated..."
    s = simple_test.simple_gen_do(n-1)
    print"s is generated..."
    with open(Xfile, 'wb') as f:
            f.write(bytes(s))
            
    int2 = bigNum.bigNum(2)
    v = bigNum.to_pow(s,int2,n)
    
    return n,v

def check(n, v, s):    #main action
    random.seed()
    t = 30
    for i in range(t):
        r = bigNum.random_big(n-1)
        int2 = bigNum.bigNum(2)
        x = bigNum.to_pow(r,int2,n)

        e = random.randint(0,1)
        if e == 0:
            y = r
        else:
            y = (r * s) % n
        
        int0 = bigNum.bigNum(0)
        if y == int0:
            return False

        sqY = bigNum.to_pow(y,int2,n)
        
        if e == 0:
            val = x
        else:
            val = (x * v) % n
        
        if sqY != val:
            return False

        print"round",i+1,"is done!"

    return True    

def main():
    parser = create_Parser()
    args = parser.parse_args(sys.argv[1:])

    n, v = pre_stage(args.secret)
    print"n=",n
    print"v=",v

    with open(args.secret, 'rb') as file:
        xfile = file.read()

    secret = bigNum.bigNum(xfile)
    
    if check(n, v, secret):
        print"Confirm!"
    else:
        print"Reject!"
            
if __name__=='__main__':
    main()
