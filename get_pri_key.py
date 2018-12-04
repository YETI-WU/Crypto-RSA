# get_private_key.py
"""
given a RSA public key, get the private key.
"""
import json
import sys
import hashlib
import math

def get_factors(n):
    p = 0
    q = 0
   
    # Fermat's Factorization Method
    a = math.ceil(math.sqrt(n))
    b2 = a**2 - n
    while not math.sqrt(b2).is_integer():
        a += 1
        b2 = a**2 - n
    print('result : a = {}, b2 = {}'.format(a,b2))
    p = int( a + math.sqrt(b2) )
    q = int( a - math.sqrt(b2) )
    print('n = {} : p = {}, q = {}'.format(n,p,q))
    return p, q



def get_key(p, q, e):
    d = 0
    # Extended Euclidean Algorithms (two value are coprime)
    totient = (p-1) * (q-1)
    m = totient
    y , x = 0 , 1
    while e > 1:
        q = e // m  # quotient
        t = m
        
        m = e % m
        e = t
        t = y
        
        y = x - q * y
        x = t
        
    if x < 0 :
        x = x + totient
        
    d = x

    return d


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        
    n , e , all_key = 0 , 0 , None
    with open("keys4student.jason", "r") as f:
        all_keys = json.load(f)
    
    name = hashlib.sha224(sys.argv[1].encode('utf-8').strip()).hexdigest()
    if name not in all_keys:
        print(sys.argv[1] + ' not in keylist')
        usage()
        
    pub_key = all_keys[name]
    n = int(pub_key['N'], 16)
    e = int(pub_key['e'], 16)
    print('Your public key: (' + hex(n).rstrip('L') + ', ' + hex(e).rstrip('L') + ')')
    
    # find p & q value that n = p * q
    (p,q) = get_factors(n)
    
    # Use p, q, e, to find the value d (Burte Force will take a long long time)
    d = get_key(p,q,e)
    
    print('Your private eky: ' + hex(d).rstrip('L') )
    

