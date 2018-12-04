# find_waldo.py
"""
given a public key P, 
find your Waldo among your classmates and get P's private key.
"""
import json
import sys
import hashlib
import math



def usage():
    print("""Usage:
    python find_waldo.py student_id (i.e., qchenxiong3)""")
    sys.exit(1)


#TODO -- n1 and n2 share p or q?
def is_waldo(n1, n2):
    result = False

    #your code can start here
    if math.gcd(n1,n2) != 1:
        result = True

    #your code ends here

    return result


#TODO -- get private key of n1
def get_private_key(n1, n2, e):
    d = 0

    #your code starts here
    
    # Extended Euclidean Algorithms (two value are coprime)
    c = math.gcd(n1,n2)
    p , q = n1//c , n2//c
    print('c = {}'.format(c))
    print('n1 = {}\np = {}'.format(n1,p))
    print('n2 = {}\nq = {}'.format(n2,q))
    totient = (p-1) * (c-1)
    #totient = (n1-1) * (n2-1)
    print('gcd(e,totient) = {}'.format(math.gcd(e,totient)))
    
    m = totient
    x , y = 1 , 0
    while e > 1:
        q = e // m  # quotient
        t = m
        
        m , e , t = e % m , t , y
        
        y = x - q * y
        x = t
        
    if x < 0 :
        x = x + totient
        
    d = x

    #your code ends here

    return d


if __name__ == "__main__":
    #if len(sys.argv) != 2:  usage()
    #student_id = 'ywu750'
    student_id = 'bdornier3'

    all_keys = None
    with open('keys4student.json', 'r') as f:
        all_keys = json.load(f)

    #name = hashlib.sha224(sys.argv[1].encode('utf-8').strip()).hexdigest()
    name = hashlib.sha224(student_id.encode('utf-8').strip()).hexdigest()
    if name not in all_keys:
        print(sys.argv[1] + ' not in keylist')
        usage()

    pub_key = all_keys[name]
    n1 = int(pub_key['N'], 16)
    e = int(pub_key['e'], 16)
    d = 0
    waldo = "Dolores"
    
    print('n1 = {}\nlen(n1) = {}\ne = {}\nlen(e) = {}'.format(n1,len(str(n1)),e,len(str(e)))) ##### Added for testing

    print("Your public key n1: (" + hex(n1).rstrip("L") + ", " + hex(e).rstrip("L") + ")")

    for classmate in all_keys:
        if classmate == name:
            continue
        n2 = int(all_keys[classmate]['N'], 16)

        if is_waldo(n1, n2):
            waldo = classmate
            d = get_private_key(n1, n2, e)
            break
    
    print('d = {}\nlen(d) = {}'.format(d,len(str(d)))) ##### Added for testing
    print("Your private key d : " + hex(d).rstrip("L"))
    print("Your waldo: " + waldo)


# (to be continued .................... )
