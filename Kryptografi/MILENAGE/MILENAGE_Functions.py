from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
#a2b & b2a - Python implementation Hints
#Takes input on the "465b5ce8 b199b49f aa5f0a2e e238a6bc" form and converts it into a bytes object
#The input should conform to the format provided in TS 35.207 & TS 35.208 for test data
#a2b: ascii-to-bytes
def a2b(s: str) -> bytes: #Developed from BTS4410-MILENAGE_2.pdf
    """Ascii to bytes. Require even length on string. """
    s = s.replace(" ","").strip()
    assert(len(s) % 2 == 0)
    bytelist = list()
    for i in range(0,len(s),2):
        bytelist.append(int("0x"+s[i]+s[i+1],16))
    return bytes(bytelist)

# Takes a bytes object as input
# The output conform to the format provided in TS 35.207 & TS 35.208 for test data.
# b2a: bytes-to-ascii
def b2a(b: bytes) -> str: #Developed from BTS4410-MILENAGE_2.pdf
    """Bytes to ASCII, a la TS 35.207//208 test data."""
    hexdig = "0123456789abcdef"
    assert(len(b) > 0)
    #hexstr = Bites(b).hex
    hexstr = ""
    for byte in b:
        lo = hexdig[byte & 0x0F]
        hi = hexdig[byte >> 4]
        hexstr += hi+lo

    # our "default"
    if len(hexstr) == 32:
        hexstr = hexstr[0:8] + " " + hexstr[8:16] + " " + hexstr[16:24] + " " + hexstr[24:]
    else:
        hs = ""
        while len(hexstr)>=8:
            hs = hs + hexstr[0:8] + " "
            hexstr = hexstr[8:]
        hexstr = hs + hexstr
    return(hexstr)

def IN1(a: bytes,b:bytes) -> bytes: #Developed from BTS4410-MILENAGE_2.pdf
   return a+b+a+b

def xor(a,b: bytes) -> bytearray: #Developed from BTS4410-MILENAGE_2.pdf
    """xor bytes objects, must be the same length"""
    assert(len(a) == len(b)), "xor -- input a must be the same size"

    result = bytearray(16)

    for i in range(len(result)):
        result[i] = a[i] ^ b[i]
    print(result)
    return result

def rotation(a:bytes, n: int) -> bytes: #Github Co-pilot helped develop this
    assert len(a) == 16, "Data must be 16 bytes"

    bitlen = 16 * 8
    n = n % bitlen

    val = int.from_bytes(a, "big")
    # Rotate left
    rotating = ((val << n) | (val >> (bitlen - n))) & ((1 << bitlen) - 1)
    # Convert back to bytes
    return rotating.to_bytes(16, "big")

def setbits(b:int) -> bytearray: #Github Co-pilot helped develop this
    assert 0 <= b < 128,"Bits must be between 0 and 128"
    data = bytearray(16)

    byte_posistion = b // 8
    bit_posistion = 7 - (b % 8)

    data[byte_posistion] = 1 << bit_posistion

    return data

def E(k,m: bytes) -> bytes: #Developed from BTS4410-MILENAGE_2.pdf
    assert(len(m) == 16),format(len(m))
    assert(len(k) == 16)

    encryptor = Cipher(algorithms.AES128(k),modes.ECB()).encryptor()
    return(encryptor.update(m) + encryptor.finalize())