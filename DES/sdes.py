# Simplified DES (Data Encryption Standard) 
# S-DES Algorithm Template Code for CNU Information Security 2022

# This code requires "bitarray" package.
# Install with: pip install bitarray

from ctypes import ArgumentError
import re
from bitarray import bitarray, util as ba_util

# Initial Permutation (IP)
IP = [ 1, 5, 2, 0, 3, 7, 4, 6 ]

# Inverse of Initial Permutation (or Final Permutation)
IP_1 = [ 3, 0, 2, 4, 6, 1, 7, 5]

# Expansion (4bits -> 8bits)
EP = [ 3, 0, 1, 2, 1, 2, 3, 0 ]

# SBox (S0)
S0 = [
    [ 1, 0, 3, 2 ],
    [ 3, 2, 1, 0 ],
    [ 0, 2, 1, 3 ],
    [ 3, 1, 3, 2 ]
]

# SBox (S1)
S1 = [
    [ 0, 1, 2, 3 ],
    [ 2, 0, 1, 3 ],
    [ 3, 0, 1, 0 ],
    [ 2, 1, 0, 3 ]
]

# Permutation (P4)
P4 = [ 1, 3, 2, 0 ]

# Permutation (P10)
P10 = [ 2, 4, 1, 6, 3, 9, 0, 8, 7, 5 ]

# Permutation (P8)
P8 = [ 5, 2, 6, 3, 7, 4, 9, 8 ]

#### DES Start

MODE_ENCRYPT = 1
MODE_DECRYPT = 2

'''
schedule_keys: generate round keys for round function
returns array of round keys.
keep in mind that total rounds of S-DES is 2.
'''
def schedule_keys(key: bitarray) -> list:
    round_keys = []
    permuted_key = bitarray()

    for i in P10:
        permuted_key.append(key[i])

    permuted_key_left = permuted_key[0:5]
    permuted_key_right = permuted_key[5:10]

    for i in range(1, 3):
        # shift for each round
        # round 1: shift 1, round 2: shift 2
        # shifting will be accumulated for each rounds
        permuted_key_left = permuted_key_left[i:] + permuted_key_left[0:i]
        permuted_key_right = permuted_key_right[i:] + permuted_key_right[0:i]

        # merge and permutate with P8
        merge_permutation = permuted_key_left + permuted_key_right
        round_key = bitarray()

        for j in P8:
            round_key.append(merge_permutation[j])

        round_keys.append(round_key)

    return round_keys

'''
round: round function
returns the output of round function
'''
def round(text: bitarray, round_key: bitarray) -> bitarray:
    # implement round function
    expanded = bitarray()
    for i in EP:
        expanded.append(text[i])
    expanded ^= round_key

    # S0
    s0_row = expanded[0:4]
    s0_sel_row = (s0_row[0] << 1) + s0_row[3]
    s0_sel_col = (s0_row[1] << 1) + s0_row[2]
    s0_result = ba_util.int2ba(S0[s0_sel_row][s0_sel_col], length=2)

    # S1
    s1_row = expanded[4:8]
    s1_sel_row = (s1_row[0] << 1) + s1_row[3]
    s1_sel_col = (s1_row[1] << 1) + s1_row[2]
    s1_result = ba_util.int2ba(S1[s1_sel_row][s1_sel_col], length=2)

    pre_perm4 = s0_result + s1_result
    
    result = bitarray()
    for i in P4:
        result.append(pre_perm4[i])

    return result

'''
sdes: encrypts/decrypts plaintext or ciphertext.
mode determines that this function do encryption or decryption.
MODE_ENCRYPT or MODE_DECRYPT available.
'''
def sdes(text: bitarray, key: bitarray, mode) -> bitarray:
    permutedText = bitarray()
        
    # IP 대로 입력을 섞는다.
    for idx in IP:
        permutedText.append(text[idx])
    
    # 입력을 left, right로 나눈다.    
    permutedTextLeft = permutedText[0:4]
    permutedTextRight = permutedText[4:8]
    
    # Key를 생성한다.
    key = schedule_keys(key)
    
    # Encryption     
    if mode == 1:
        # Right을 1 Round Key를 넣어 F에 통과시킨 후,
        afterRound1 = round(permutedTextRight, key[0])
        # Left 와 XOR 연산을 취한다.
        afterRound1 ^= permutedTextLeft
        
        # Right 와 F를 통과한 Right에 Left을 XOR 한 값을 합쳐서 다음 라운드 진행
        # Switch된 Right 에 2 Round Key를 통과시키고, 
        afterRound2 = round(afterRound1, key[1])
        # Switch된 Left 와 XOR 연산을 취한다.
        afterRound2 ^= permutedTextRight
        
        afterRound = afterRound2 + afterRound1
        
    # Decryption : Encryption과 Key 넣는 순서만 반대로 바꾼다.
    else:
        afterRound1 = round(permutedTextRight, key[1])
        afterRound1 ^= permutedTextLeft
        
        afterRound2 = round(afterRound1, key[0])
        afterRound2 ^= permutedTextRight
        
        afterRound = afterRound2 + afterRound1
            
    result = bitarray()
    # 마지막 결과를 Inverse IP 대로 재배치하여 반환한다.
    for idx in IP_1:
        result.append(afterRound[idx])        
        
    return result

#### DES Sample Program Start

plaintext = input("[*] Input Plaintext in Binary (8bits): ")
key = input("[*] Input Key in Binary (10bits): ")

# Plaintext must be 8 bits and Key must be 10 bits.
if len(plaintext) != 8 or len(key) != 10:
    raise ArgumentError("Input Length Error!!!")

if re.search("[^01]", plaintext) or re.search("[^01]", key):
    raise ArgumentError("Inputs must be in binary!!!")

bits_plaintext = bitarray(plaintext)
bits_key = bitarray(key)

print(f"Plaintext: {bits_plaintext}")
print(f"Key: {bits_key}")

result_encrypt = sdes(bits_plaintext, bits_key, MODE_ENCRYPT)

print(f"Encrypted: {result_encrypt}")

result_decrypt = sdes(result_encrypt, bits_key, MODE_DECRYPT)

print(f"Decrypted: {result_decrypt}, Expected: {bits_plaintext}")

if result_decrypt != bits_plaintext:
    print(f"S-DES FAILED...")
else:
    print(f"S-DES SUCCESS!!!")
    
    
'''
01011111
1101110111
'''

'''
11101110
0000100001
'''