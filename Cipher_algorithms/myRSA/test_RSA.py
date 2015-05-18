import myRSA
import bigNum

def testRSA ():
    with open('C:\RSA\encrypted_data.txt', 'rb') as file:
        msg = file.read()
    with open('C:\RSA\private_key.txt', 'rb') as f:
        dd = f.readline()
        nn = f.readline()

    c = bigNum.bigNum(msg)
    d = bigNum.bigNum(dd[:len(dd)-1])
    n = bigNum.bigNum(nn)

    m = myRSA.decrypt(c,d,n)
    
    with open('C:\RSA\data.txt', 'rb') as filename:
        tmp = filename.read()

    data = bigNum.bigNum(tmp[3:])

    assert m == data
