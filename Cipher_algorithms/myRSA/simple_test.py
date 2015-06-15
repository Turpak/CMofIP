#!/usr/bin/env python
import BigInt
import argparse
import sys

BigInt.initRandom()

def step(a, t, m, s):
    x = BigInt.powmod(a, t, m)
    
    if x == 1 or x == m - 1:
        return True

    i = BigInt.BigInt(0)
    while i < s - 1:
        x = (x * x) % m
        if x == m - 1:
            return True
        if x == 1:
            return False
        s = s - 1
    
    return x == m - 1    
    

def miller_test(m):#m - bigNum
    if m % 2 == 0:
        return False

    t = m - 1
    s = BigInt.BigInt(0)

    while t % 2 == 0:
        t /= 2
        s += 1
    
    for rnd in range(20):
        a = BigInt.random_big(m - 4) + 2
        if not step(a, t, m, s):
            return False

    return True

def simple_gen(len):
    gen_res = BigInt.random_fixlen(len)

    if gen_res % 2 == 0:
        gen_res += 1
    
    while not miller_test(gen_res):
        gen_res += 2

    return gen_res
