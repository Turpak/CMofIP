import myRSA
import bigNum
import keygen

def testRSA ():
    e, d, n = keygen.keygen() 
    m = bigNum.random_big(n-10)

    c = myRSA.encrypt(m,e,n)
    data = myRSA.decrypt(c,d,n)

    assert m == data
