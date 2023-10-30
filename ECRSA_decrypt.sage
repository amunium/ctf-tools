from Crypto.Util.number import bytes_to_long
from Crypto.Util.number import long_to_bytes
long_to_bytes(42134526936699777519202942313470556891460166896482958779251517309)

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
F = GF(p)
print("p = ", p)
secp256k1 = EllipticCurve(GF(p), [0, 7]) 
print("secp256k1 = ", secp256k1)
print("secp256k1.order() = ", secp256k1.order())
    
e = 65537
flag = b"flag{thisad}"
m = bytes_to_long(flag)
print("m = ", m)

G = secp256k1.lift_x(F(m))
print("G = ", G)

ct = e*G
print(f"ct = {ct.xy()}")


print("Starting decrypt")

# d = e^1 mod secp256k1.order()
d = 92190906271479038726315065181017232156693337603458343161572162405378277135252
print("d = ", d)
 
plaintext = ct*d
print("ct*int(d) = pt = ", plaintext)
print("G == pt : ", plaintext == G)
if plaintext == G:
    print("Deryption succsessfull!")
else:
    print("Decryption failed.")