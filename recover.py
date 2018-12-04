# recover.py
"""
A message was encrypted with three different 1024 bit RSA public keys, 
all of them have the public exponent e = 3, 
resulting in three different encrypted messages. 
Given the three pairs of public keys and encrypted messages, 
recover the original message.
"""
import json
import sys
import hashlib
import math



#from gmpy2 import root
# https://cryptologie.net/article/182/airbus-crypto-challenge-write-up/
## extended euclide algorithm
def xgcd(a,b):
    #Extended GCD:
    #Returns (gcd, x, y) where gcd is the greatest common divisor of a and b
    #with the sign of b if b is nonzero, and with the sign of a if b is 0.
    #The numbers x,y are such that gcd = ax+by.
    prevx, x = 1, 0;  prevy, y = 0, 1
    while b:
        q, r = divmod(a,b)
        x, prevx = prevx - q*x, x  
        y, prevy = prevy - q*y, y
        a, b = b, r
    return a, prevx, prevy

""" myself code
def xgcd(t,e):
    m = t
    x , y = 1 , 0
    while e > 1:
        q = e // m  # quotient
        t = m
        m , e , t = e % m , t , y
        y = x - q * y
        x = t
    if x < 0 :
        x = x + t
    d = x
    return d
"""

def cubeRoot(num):
    high = 1
    while high **3 < num:
        high *= 2
    low = high//2
    while low < high:
        mid = (low+high) // 2
        if low < mid and mid**3 < num :
            low = mid
        elif high > mid and mid**3 > num:
            high = mid
        else:
            return mid
    return mid + 1


#TODO
def recover_msg(N1, N2, N3, C1, C2, C3):

    m = 42
    # your code starts here: to calculate the original message - m
    # Note 'm' should be an integer
    
    N2N3 = N2 * N3
    N1N3 = N1 * N3
    N1N2 = N1 * N2
    
    N2N3_ = xgcd(N2N3, N1)[1]
    N1N3_ = xgcd(N1N3, N2)[1]
    N1N2_ = xgcd(N1N2, N3)[1]
    """ myself code
    N2N3_ = xgcd(N2N3, N1)
    N1N3_ = xgcd(N1N3, N2)
    N1N2_ = xgcd(N1N2, N3)
    """
    m3 = C1 * N2N3 * N2N3_ + C2 * N1N3 * N1N3_ + C3 * N1N2 * N1N2_
    m3 = m3 % (N1 * N2 * N3)
    
    print('m3 = {}'.format(m3))
    print('len(m3) = {}'.format(len(str(m3))))
    
    
    m = int(cubeRoot(m3))
    #m = int(root(m3, 3)) # aaossa code

    # your code ends here
    
    # convert the int to message string
    msg = bytes.fromhex(hex(m).rstrip('L')[2:]).decode('utf-8')
    ### aaossa coding
    # M = hex(M)[2:]
    # print(unhexlify(M).decode('utf-8'))
    return msg


if __name__ == "__main__":
    #if len(sys.argv) != 2:  usage()
    student_id = 'ywu750'
    #student_id = 'bdornier3'

    all_keys = None
    with open('keys4student.json', 'r') as f:
        all_keys = json.load(f)

    #name = hashlib.sha224(sys.argv[1].encode('utf-8').strip()).hexdigest()
    name = hashlib.sha224(student_id.encode('utf-8').strip()).hexdigest()
    """
    if name not in all_keys:
        print(sys.argv[1] + ' not in keylist')
        usage()
    """
    data = all_keys[name]
    N1 = int(data['N0'], 16)
    N2 = int(data['N1'], 16)
    N3 = int(data['N2'], 16)
    C1 = int(data['C0'], 16)
    C2 = int(data['C1'], 16)
    C3 = int(data['C2'], 16)
    print('N1 = {}\nN2 = {}\nN3 = {}'.format(N1,N2,N3))
    print('len(N1) = {} , len(N2) = {} , len(N3) = {}'.format(len(str(N1)),len(str(N2)),len(str(N3))))
    print('C1 = {}\nC2 = {}\nC3 = {}'.format(C1,C2,C3))    
    print('len(C1) = {} , len(C2) = {} , len(C3) = {}'.format(len(str(C1)),len(str(C2)),len(str(C3))))
    
    print('gcd(N1,N2) = {}, gcd(N2,N3) = {}, gcd(N3,N1) = {}'.format(math.gcd(N1,N2),math.gcd(N2,N3),math.gcd(N3,N1)))
    msg = recover_msg(N1, N2, N3, C1, C2, C3)
    print(msg)



# ( To be continue .................... )
