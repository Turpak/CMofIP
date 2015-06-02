#!/usr/bin/env python3

import myGost3411
from subprocess import Popen, PIPE
from hypothesis import given

@given(str)		
def test_gost3411_94(data):
    command = ['openssl', 'dgst', '-hex', '-md_gost94']
    proc = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    res, err = proc.communicate(input=data)
    res = res[9:-1]
    
    assert  res == myGost3411.hash_in_hex(myGost3411.gost3411(data))
