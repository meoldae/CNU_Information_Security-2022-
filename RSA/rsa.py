# BigNumber, mpmath package required
# run this before execute: pip install BigNumber mpmath

import random
import BigNumber

# https://www.delftstack.com/howto/python/python-generate-prime-number/
def primesInRange(x, y):
    prime_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False

        if isPrime:
            prime_list.append(n)
            
    return prime_list

def make_keys(p: BigNumber, q: BigNumber):
    # place your own implementation of make_keys
    # use e = 65537 as if FIPS standard
    n = p * q
    phiN = (p-1)*(q-1)
    d = 0
    e = 65537
    
    NumForCount = random.randrange(1, 10)
    count = 0

    # d*e mod phiN 이 1이면, count + 1
    # random Count 번째에서 mod 연산을 만족하면서 
    # e와 같지 않은 값의 d로 설정
    while count < NumForCount:
        if ((d * e) % phiN == 1) and (d != e):
            count += 1
        else:
            d += 1
    
    return [e, d, n]

def rsa_encrypt(plain: BigNumber, e: BigNumber, n: BigNumber):
    c = (plain**e)%n
    return c

def rsa_decrypt(cipher: BigNumber, d: BigNumber, n: BigNumber):
    m = (cipher**d)%n
    return m

primes = primesInRange(100, 1000)

P = primes[random.randrange(0, len(primes))]
Q = primes[random.randrange(0, len(primes))]

while P == Q:
    P = primes[random.randrange(0, len(primes))]
    Q = primes[random.randrange(0, len(primes))]

M = random.randrange(2, 20)
e, d, N = make_keys(P, Q)
C = rsa_encrypt(M, e, N)
M2 = rsa_decrypt(C, d, N)

print(f"P = {P}, Q = {Q}, N = {N}, M = {M}, e = {e}, d = {d}, C = {C}, M2 = {M2}")

if M == M2:
    print("RSA Success!!")
else:
    print("RSA Failed...")
