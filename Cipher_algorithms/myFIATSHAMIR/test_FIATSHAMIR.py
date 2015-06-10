import myFIATSHAMIR
import bigNum

def test_truePASSWORD ():
    Xfile = 'secret.txt'
    n, v = myFIATSHAMIR.pre_stage(Xfile)

    with open(Xfile, 'rb') as file:
        xfile = file.read()

    secret = bigNum.bigNum(xfile)
     
    assert True == myFIATSHAMIR.check(n, v, secret)

def test_wrongPASSWORD ():
    secret = 'secret.txt'
    n, v = myFIATSHAMIR.pre_stage(secret)

    wrong_secret = bigNum.random_big(n-1)

    assert False == myFIATSHAMIR.check(n, v, wrong_secret)
