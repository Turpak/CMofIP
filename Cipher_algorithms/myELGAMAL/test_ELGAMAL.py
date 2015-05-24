import myELGAMAL
import bigNum

def testELGAMAL ():
    with open('C:\ELGAMAL\encrypted_data.txt', 'rb') as file:
        aa = file.readline()
        bb = file.readline()
    with open('C:\ELGAMAL\private_key.txt', 'rb') as f:
        xx = f.readline()
        pp = f.readline()
                
    a = bigNum.bigNum(aa[:len(aa)-1])
    b = bigNum.bigNum(bb)
    x = bigNum.bigNum(xx[:len(xx)-1])
    p = bigNum.bigNum(pp)

    M = myELGAMAL.decrypt(a,b,x,p)
    
    with open('C:\ELGAMAL\data.txt', 'rb') as filename:
        tmp = filename.read()

    data = bigNum.bigNum(tmp[3:])

    assert M == data
