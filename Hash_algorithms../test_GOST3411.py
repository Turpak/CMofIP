#!/usr/bin/env python3

import myGost3411
from subprocess import Popen, PIPE

def gost_rhash (fileName):
    command = [r'C:\Users\PC\rhash.exe','--gost', fileName]

    proc = Popen(command, shell=False, stdout=PIPE, stderr=PIPE)
    proc.wait()

    res = proc.communicate()

    h = res[0]
    result = h[0:64]

    return result
    
def test1():
    fileName1 = 'C:\Labs\myGostin1.txt'
    with open(fileName1, 'rb') as f:
        data = f.read()
    m = gost_rhash(fileName1)
    
    x = bytes(myGost3411.hash_in_hex(myGost3411.gost3411(data)), encoding='utf-8')
        
    assert m == x

def test2():
    fileName2 = 'C:\Labs\myGostin2.txt'
    with open(fileName2, 'rb') as f:
        data = f.read()
    m = gost_rhash(fileName2)
    
    x = bytes(myGost3411.hash_in_hex(myGost3411.gost3411(data)), encoding='utf-8')
        
    assert m == x

def test3():
    fileName3 = 'C:\Labs\myGostin3.txt'
    with open(fileName3, 'rb') as f:
        data = f.read()

    m = gost_rhash(fileName3)
    x = bytes(myGost3411.hash_in_hex(myGost3411.gost3411(data)), encoding='utf-8')
        
    assert m == x

def test4():
    fileName4 = 'D:\Sborka.txt'
    with open(fileName4, 'rb') as f:
        data = f.read()

    m = gost_rhash(fileName4)
    x = bytes(myGost3411.hash_in_hex(myGost3411.gost3411(data)), encoding='utf-8')
        
    assert m == x
