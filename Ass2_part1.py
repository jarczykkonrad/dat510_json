from des import DesKey
from random import randint

def computing_mod(a,b,n):
    return int(pow(a,b,n))

#Generating prime numbers which mod 4 = 3. Needed for Blum Blum Shub
def generate_prime():
    prime = randint(1000,100000)
    for j in range(2, int(prime/2)+1):
        if prime % j == 0 or prime % 4 != 3:
            prime = generate_prime()
            break
    return prime

# Blum Blum Shub Generator using 56 bits converted to hexadecimals PRNGD
def bbs(seed, M):
    output= ""
    x = seed
    for _ in range(56):
        x = computing_mod(x,2,M)
        b = x % 2
        output+=str(b)
    if len(hex(int(output,2))) != 16:
        raise("Regenerate prime numbers!")
    #print(output) for binary look
    return hex(int(output,2))

def encryption_DES(plaintext, key):
    key = DesKey(bytes(key.encode('utf-8')))
    cipher = key.encrypt(bytes(plaintext.encode('utf-8')), padding=True)
    return cipher

def decryption_DES(cipher, key):
    key = DesKey(bytes(key.encode('utf-8')))
    plaintext = key.decrypt(bytes(cipher), padding=True)
    return plaintext

# for server part
def getpub_Alice(g=None, prime_number_1=None, prime_number_2 = None):
    if g == None:
        g=2
        prime_number_1 = generate_prime()
        prime_number_2 = generate_prime()
    PRa = randint(1000, 10000)
    PUa = computing_mod(g, PRa, prime_number_1)
    return PRa, PUa, g, prime_number_1, prime_number_2

# for server part
def getpub_Bob(g=None, prime_number_1=None, prime_number_2=None ):
    if g==None:
        g = 2
        prime_number_1 = generate_prime()
        prime_number_2 = generate_prime()
    PRb = randint(1000, 10000)
    PUb = computing_mod(g, PRb, prime_number_1)
    return PRb, PUb, g, prime_number_1, prime_number_2

if __name__ == "__main__":
    g=2
    prime_number_1=generate_prime()
    prime_number_2= generate_prime()
    n = prime_number_1 * prime_number_2
    print("The value of cyclic group: g=%s" % g)
    print("The value of first prime number: %s" % prime_number_1)
    print("The value of second prime number: %s" % prime_number_2)
    print("The value of n = %s, for Blum Blum Shub generator mod" % n)
    print()
    #private key  and public key Alice
    PRa = randint(1000,10000)
    PUa = computing_mod(g, PRa, prime_number_1)
    print("Alice's public key: %s" % PUa)
    #private key and public key Bob
    PRb = randint(1000,10000)
    PUb = computing_mod(g, PRb, prime_number_1)
    print("Bob's public key: %s" % PUb)
    Kab_1 = computing_mod(PUb, PRa, prime_number_1)
    Kab_2 = computing_mod(PUa, PRb, prime_number_1)
    if Kab_1 == Kab_2:
        Kab=Kab_1=Kab_2
    print("Bob's and Alice's shared key: %s" % Kab)

    secret_key = bbs(Kab,n)
    print("Secret key after PRNG (BBS generator for 56 bits, 16 bytes Hexadecimal): %s" % secret_key)
    print()
    plaintext_a = input("Hey ALice! Please write your message here: ")
    cipher = encryption_DES(plaintext_a, secret_key)
    print("Encrypted message with DES: %s, sent to Bob" % cipher)
    decoded_message = decryption_DES(cipher, secret_key).decode('utf-8')
    print("Encrypted message with DES by Bob: %s" % decoded_message)





