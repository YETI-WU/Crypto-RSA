# get_prime_key.py


def get_factors(n):
    p = 0
    q = 0
   
    # Fermat's Factorization Method
    a = math.ceil(math.sqrt(n))
    b2 = a**2 - n
    while not math.sqrt(b2).is_integer():
        a += 1
        b2 = a**2 - n
    #print('result : a = {}, b2 = {}'.format(a,b2))
    p = int( a + math.sqrt(b2) )
    q = int( a - math.sqrt(b2) )
    #print('n = {} : p = {}, q = {}'.format(n,p,q))

    return p, q



def get_key(p, q, e):
    d = 0
    # Extended Euclidean Algorithms (two value are coprime)
    totient = (p-1) * (q-1)
    m = totient
    y = 0
    x = 1
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
