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

def main():
    p = simple_test.simple_gen(100)
    print"p=",p
    g = simple_test.simple_gen_do(p)
    print"g=",g
    x = bigNum.random_big(p)
    print"x=",x
    y = bigNum.to_pow(g, x, p)
    print"y=",y
    
    parser = create_Parser()
    args = parser.parse_args(sys.argv[1:])

    args.public.write(bytes(p) + '\n' + bytes(g) + '\n' + bytes(y))
    args.private.write(bytes(x))

if __name__=='__main__':
    main()
