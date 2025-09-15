# Ron was wrong, Whit was right (cryptohack)
# https://eprint.iacr.org/2012/064.pdf

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import hashes
import math

fileLocation = "../../workFolder/keys_and_messages/" # End with /
extension = ".pem"
ctr = 0

keyList = []


# Load all PEM keys into a list for easier working later.
while True:
    ctr += 1

    keyFile = f"{fileLocation}{ctr}{extension}" 

    try:
        with open(keyFile, "rb") as pemFile:
            key_data = pemFile.read()
            key = load_pem_public_key(key_data)
            keyList.append(key)
            
    # Exit when an invalid name is reached.
    except FileNotFoundError: 
        print("Exit loop. Reached invalid name:", keyFile)
        break


# Get private key
def getPrivateKey(n, p, e):
    phi_n = (p-1)*(n//p - 1)
    d = pow(e, -1, phi_n)
    return d


def decryptMessage(number, n,p,q,e,d):
    print(f'The key consists of: \nn: {n} \np: {p} \nq: {q}\ne: {e}\nd: {d}\n')

    privateKey = rsa.RSAPrivateNumbers(
        p=p, 
        q=q,
        d=d,
        dmp1 = d % (p-1),
        dmq1 = d % (q-1),
        iqmp = pow(q, -1, p),
        public_numbers = rsa.RSAPublicNumbers(e, n)
    ).private_key()

    print(f'Decrypting ciphertext {number + 1}.ciphertext:')

    with open(f'{fileLocation}{number + 1}.ciphertext', "r") as ctx:
        ciphertext = bytes.fromhex(ctx.read())
        message = privateKey.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),  # OAEP padding as specified in provided code
                algorithm=hashes.SHA1(),
                label=None
            )
        )
        print(f'{message}')



# Go through list and for each key, check if all the next keys in the list share any non-trivial primes.
for a in range(len(keyList)):
    for b in range(a + 1, len(keyList)):
        gcd_value = math.gcd(keyList[a].public_numbers().n, keyList[b].public_numbers().n)
        if gcd_value != 1:
            print(f'The keys {a + 1}{extension} and {b + 1}{extension} share a common prime of: \n{gcd_value}')

            a_d = getPrivateKey(keyList[a].public_numbers().n, gcd_value, keyList[a].public_numbers().e)
            print(f'\n{a + 1}{extension}:')
            decryptMessage(a, keyList[a].public_numbers().n, keyList[a].public_numbers().n//gcd_value, gcd_value, keyList[a].public_numbers().e, a_d)


            b_d = getPrivateKey(keyList[b].public_numbers().n, gcd_value, keyList[b].public_numbers().e)
            print(f'\n{b + 1}{extension}:')
            decryptMessage(b, keyList[b].public_numbers().n, gcd_value, keyList[b].public_numbers().n//gcd_value, keyList[b].public_numbers().e, b_d)

