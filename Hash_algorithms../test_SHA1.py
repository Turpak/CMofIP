import mySHA1
import hashlib

def testSHA1_1 ():
    test_text = b"qwertyone qwertytwo qwertythree qwertyfour qwertyfive yeah"
    m = hashlib.sha1(test_text).hexdigest()
    
    assert m == mySHA1.hash_in_hex(mySHA1.sha1(test_text))

def testSHA1_2 ():
    test_text = b""
    m = hashlib.sha1(test_text).hexdigest()
    
    assert m == mySHA1.hash_in_hex(mySHA1.sha1(test_text))

def testSHA_3 ():
    test_text = b"The quick brown fox jumps over the lazy dog"
    m = hashlib.sha1(test_text).hexdigest()
    
    assert m == mySHA1.hash_in_hex(mySHA1.sha1(test_text))
