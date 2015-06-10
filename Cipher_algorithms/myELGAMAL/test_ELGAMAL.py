import random
import pytest
import myELGAMAL
import bigNum
import simple_test

def testELGAMAL ():
    p = simple_test.simple_gen(50)
    g = simple_test.simple_gen_do(p)
    x = bigNum.random_big(p)
    y = bigNum.to_pow(g, x, p)

    M = bigNum.random_big(p-10)

    a, b = myELGAMAL.encrypt(M,p,g,y)
    data = myELGAMAL.decrypt(a,b,x,p)

    assert M == data
