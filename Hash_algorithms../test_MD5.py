import myMD5
import hashlib

def testMD51 ():
    test_text = b"blablacar"
    m = hashlib.md5(test_text).hexdigest()
    
    assert m == myMD5.hash_in_hex(myMD5.md5(test_text))

def testMD52 ():
    test_text = b""
    m = hashlib.md5(test_text).hexdigest()
    
    assert m == myMD5.hash_in_hex(myMD5.md5(test_text))

def testMD53 ():
    test_text = b"my life, my rules"
    m = hashlib.md5(test_text).hexdigest()
    
    assert m == myMD5.hash_in_hex(myMD5.md5(test_text))
