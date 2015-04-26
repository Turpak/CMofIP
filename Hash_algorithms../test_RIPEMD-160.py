import myRipeMD160
import hashlib
import os

def testRipeMD1601 ():
    test_text = os.urandom(32)
    print(test_text)
    m = hashlib.new('ripemd160')
    m.update(test_text)
    m = m.hexdigest()
    
    assert m == myRipeMD160.hash_in_hex(myRipeMD160.ripemd160(test_text))

def testRipeMD1602 ():
    test_text = os.urandom(64)
    m = hashlib.new('ripemd160')
    m.update(test_text)
    m = m.hexdigest()
    
    assert m == myRipeMD160.hash_in_hex(myRipeMD160.ripemd160(test_text))

def testRipeMD1603 ():
    test_text = os.urandom(200)
    m = hashlib.new('ripemd160')
    m.update(test_text)
    m = m.hexdigest()
    
    assert m == myRipeMD160.hash_in_hex(myRipeMD160.ripemd160(test_text))


