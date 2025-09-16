from MILENAGE_Functions  import *

#test data provided in TS 35.208 4.3 Test Sets
k = a2b("4ab1deb0 5ca6ceb0 51fc98e7 7d026a84") #key
m = a2b("a840b1dd 60249aa3 22016b4b 31daf3b8") #Plaintext from 3.3.2 Hexadecimal Format
xc = a2b("02bffada 7137c492 c00e8452 d8c76eaa") #Ciphertext from 3.3.2 Hexadecimal Format
op = a2b("2d16c5cd 1fdf6b22 383584e3 bef2a8d8")
RAND = a2b("74b0cd60 31a1c833 9b2b6ce2 b8c4a186")
SQN = a2b("e880a1b5 80b6")
AMF = a2b("9f07")
#R1-5 Values for Rotations
r1 = 64
r2 = 0
r3 = 32
r4 = 64
r5 = 96
#Setting Bits
c1 = bytearray(16)
c2 = setbits(127)
c3 = setbits(126)
c4 = setbits(125)
c5 = setbits(124)

#IN1 IN1 = SQN+AMF+SQN+AMF
ini = IN1(SQN,AMF)
IN1 = b2a(ini)

#OPC OPC = OP ⊕ E[OP]K.
epok = E(k,op)
OPC = xor(op,epok)

#TEMP TEMP = E[RAND ⊕ OPC]K.
OPC_bits = OPC
RAND_XOR = xor(RAND,OPC_bits)
TEMP_XOR = E(k,RAND_XOR)

#OUT1-5
#OUT1 = E[TEMP ⊕ rot(IN1 ⊕ OPC, r1) ⊕ c1]K ⊕ OPC formula used to develop OUT1
def OUT1(TEMP_XOR: bytes, ini: bytes, OPC: bytes, k: bytes, r1: int, c1: bytes) -> bytes:
    #Here we xor INI and OPC
    one = xor(ini,OPC)
    #Then we take our value from last function and rotate with R1:64
    two = rotation(one,r1)
    #Here we take our TEMP value and xor it with our new value from when we did the rotation
    three = xor(TEMP_XOR,two)
    #then we XOR with c1 from our setting bits function
    four = xor(three,c1)
    #This is the Encryption process with our defined key from k
    five = E(k,four)

    #then at last we XOR it with OPC
    result = xor(five,OPC)
    #Returns our result in a byte array
    return result

#OUT2 = E[rot(TEMP ⊕ OPC, r2) ⊕ c2]K ⊕ OPC formula used to develop OUT2
def OUT2(TEMP_XOR: bytes, OPC: bytes, k: bytes, r2: int, c2: bytes) -> bytes:
    #Here we take TEMP and OPC
    one = xor(TEMP_XOR,OPC)
    #Then we take our value from the last function and rotate with R2:0
    two = rotation(one,r2)
    #then we XOR with c2 from our setbits functions
    three = xor(two,c2)
    #this is the Encryption process with our key from k
    four = E(k,three)
    #then we at last xor the last function with OPC
    result = xor(four,OPC)
    #Returns our result in a byte array
    return result

#OUT3 = E[rot(TEMP ⊕ OPC, r3) ⊕ c3]K ⊕ OPC formula used to develop OUT3
def OUT3(TEMP_XOR: bytes, OPC: bytes, k: bytes, r3: int, c3: bytes) -> bytes:
    #Here we take TEMP and OPC
    one = xor(TEMP_XOR,OPC)
    #Then we take our value from the last function and rotate with R3:32
    two = rotation(one,r3)
    # then we XOR with c3 from our setbits functions
    three = xor(two,c3)
    #this is the Encryption process with our key from k
    four = E(k,three)
    # then we at last xor the last function with OPC
    result = xor(four,OPC)
    # Returns our result in a byte array
    return result

#OUT4 = E[rot(TEMP ⊕ OPC, r4) ⊕ c4]K ⊕ OPC formula used to develop OUT4
def OUT4(TEMP_XOR: bytes, OPC: bytes, k: bytes, r4: int, c4: bytes) -> bytes:
    # Here we take TEMP and OPC
    one = xor(TEMP_XOR,OPC)
    # Then we take our value from the last function and rotate with R4:64
    two = rotation(one,r4)
    # then we XOR with c4 from our setbits functions
    three = xor(two,c4)
    # this is the Encryption process with our key from k
    four = E(k,three)
    # then we at last xor the last function with OPC
    result = xor(four,OPC)
    # Returns our result in a byte array
    return result

#OUT5 = E[rot(TEMP ⊕ OPC, r5) ⊕ c5]K ⊕ OPC formula used to develop OUT5
def OUT5(TEMP_XOR: bytes, OPC: bytes, k: bytes, r5: int, c5: bytes) -> bytes:
    # Here we take TEMP and OPC
    one = xor(TEMP_XOR,OPC)
    # Then we take our value from the last function and rotate with R5:96
    two = rotation(one,r5)
    # then we XOR with c5 from our setbits functions
    three = xor(two,c5)
    # this is the Encryption process with our key from k
    four = E(k,three)
    # then we at last xor the last function with OPC
    result = xor(four,OPC)
    # Returns our result in a byte array
    return result

#out1 and from this we generate f1 and f1* from TS35.208
out1 = OUT1(TEMP_XOR, ini, OPC, k, r1, c1)

#out2 and from this we generate f2 and f5 from TS 35.208
out2 = OUT2(TEMP_XOR, OPC, k,r2,c2)

#out 3 and from this we generate f3 from TS 35.208
out3 = OUT3(TEMP_XOR, OPC, k,r3,c3)

#out4 and from this we generate f4 from TS 35.208
out4 = OUT4(TEMP_XOR, OPC, k,r4,c4)

#out5 and from ths we generate f5* from TS 35.208
out5 = OUT5(TEMP_XOR, OPC, k,r5,c5)

#below is the full f1-f5 answers (including *)
mac_a = out1[:8]
print("f1 (MAC-A) = ", b2a(mac_a))

mac_s = out1[8:]
print("f1* (MAC-S) = ", b2a(mac_s))

res = out2[8:]
print("f2 (RES) = ", b2a(res))

ck = out3
print("f3 (CK) = ", b2a(ck))

ik = out4
print("f4 (IK) = ", b2a(ik))

ak = out2[:6]
print("f5 (AK) = ", b2a(ak))

ak_star = out5[:6]
print("f5* (AK-STAR) = ", b2a(ak_star))