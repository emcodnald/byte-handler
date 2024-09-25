"""
byte handling module used for experiments with custom data storage
"""
import math

"""
the showBitsL function - input: positive integer, integer | output: string
takes a positive integer num and returns its value in binary using le bits
if le is less than ceil(log(num,2)), then ceil(log(num,2)) bits are used
"""
def showBitsL(num,le):
    finalString = ""
    l = max(le,math.ceil(math.log2(num)))
    for i in range(l):
        finalString += str(math.floor(num/pow(2,(l-1)-i)%2))
    return finalString

"""
the bitToDec function - input: string | output: integer ranging from 0-255
takes a binary string and returns an integer that represents its value in decimal
"""
def bitToDec(s):
    final = 0
    for i in range(len(s)):
        if s[i] == "1":
            final += pow(2,len(s)-i-1)
    return final

"""
the stream class

represents a byte stream


attributes:
    l - type: byte container
    array of numbers that represent the bytes in the stream

    b - type: string
    string of 0s and 1s that represent any bit values in the stream

functions:
    byte - input: integer ranging from 0 - 255 | no output
    takes an integer ranging from 0 - 255 and adds it to attribute l

    lInt - input: integer | no output
    takes an integer and stores it in attribute l using the following format:

        1 bit - sign | indicates whether or not the value is signed
        7 bits - length | indicator of the amount of bytes used to represent the value
        length bytes - value | denoted the value using a variable amount of bytes

        examples:
            if n = 45, then it would be stored as 00000001 00101101 in attribute l
            0 = positive indicator
            0000001 = one byte used to store the value
            00101101 = 45 in binary

            if n = -13556, then it would be stored as 10000010 00110100 11110100 in attribute l
            1 = negative indicator
            0000010 = two bytes used to store the value
            0011010011110100 = 13556 in binary

        the range of values that can be stored is -2^1016+1 to 2^1016-1
    
    fInt - input: positive integer, positive integer | no output
    takes an integer n and stores it in attribute l using le bytes
    if le is less than ceil(log(num,256)), then ceil(log(num,256)) bytes are used

    mBit - input: positive integer, positive integer | no output
    takes an integer n and stores it in attribute l using le bits
    if le is less than ceil(log(num,2)), then ceil(log(num,2)) bits are used

    sBit - input: boolean | no output
    takes a boolean and stores it as a single bit in attribute l

    flo - input: float | no output
    takes a floating point value and stores it using the following format:
    
        1 bit - sign | indicates whether or not the value is signed
        1 bit - isFloat | indicates whether or not to store the floating point. set to false for values that are either integers or close enough to integers where storing decimal values would not be possible(e.g. 56.000... or 39.999...)
        6 bits - length | indicator of the amount of bytes used to represent the whole number value
        length bytes - value | value using a variable amount of bytes
        5 bytes(optional) - decimal value | the floating point multiplied by 2^40 and stored using 5 bytes. is omitted for values close enough to whole numbers

        examples:
            if n = 77.0, then it would be stored as 00000001 01001101 in attribute l
            0 = positive indicator
            0 = the remainder is 0.0, so the extra data is not stored
            000001 = one byte used to store the whole number value
            01001101 = 77 in binary

            if n = -563.89, then it would be stored as 11000010 00000010 00110011 11100011 11010111 00001010 00111101 01110001 in attribute l
            1 = negative indicator
            1 = the remainder is 0.89, so the extra data is stored
            000010 = two bytes used to store the whole number value
            0000001000110011 = 563 in binary
            1110001111010111000010100011110101110001 = 0.89 * 2^40, rounded to the nearest integer(978,565,348,721) in binary

        the range of values that can be stored is -2^504+2^40 to 2^504-2^-40

    fill - no input | no output
    adds padding 0s to attribute l until the data is byte aligned
"""
class stream:
    def __init__(self):
        self.l = b''
        self.b = ""
    def byte(self,n):
        self.l += n.to_bytes(1,byteorder="big")
    def lInt(self,n):
        sLen = 0
        if abs(round(n)) > 0:
            sLen = math.ceil(math.log(abs(round(n)),256))
        if sLen >= 128:
            raise ValueError("value is out of range to represent(-2^1016+1 to 2^1016-1)")
        self.l += (sLen+128*(n < 0)).to_bytes(1,byteorder="big")
        for i in range(sLen):
            self.l += (math.floor(abs(round(n))/pow(256,sLen-i-1))%256).to_bytes(1,byteorder="big")
    def fInt(self,n,le):
        if n < 0 or le < 0:
            raise ValueError("either n or le is less than 0")
        l = max(le,math.ceil(math.log(n)/math.log(256)))
        for i in range(l):
            self.l += (math.floor(abs(round(n))/pow(256,l-i-1))%256).to_bytes(1,byteorder="big")
    def mBit(self,n,le):
        if n < 0 or le < 0:
            raise ValueError("either n or le is less than 0")
        sub = showBitsL(n,le)
        for i in range(len(sub)):
            self.b += sub[i]
            if len(self.b) == 8:
                self.l += (bitToDec(self.b)).to_bytes(1,byteorder="big")
                self.b = ""
    def sBit(self,s):
        if s:
            self.b += "1"
        else:
            self.b += "0"
        if len(self.b) == 8:
            self.l.append(bitToDec(self.b))
            self.b = ""
    def flo(self,n):
        floatVal = round((abs(n)%1)*pow(2,40))
        isFloat = floatVal > 0 and floatVal < pow(2,40)
        self.sBit(n < 0)
        self.sBit(isFloat)
        cLen = 0
        if abs(n) > 0:
            cLen = math.ceil(math.log(abs(n)+1, 256))
        self.mBit(cLen, 6)
        base = abs(int(n))
        if floatVal == pow(2,40):
            base += 1
        self.fInt(base, cLen)
        if isFloat:
            self.fInt(floatVal, 5)
    def fill(self):
        if len(self.b) > 0:
            while len(self.b) < 8:
                self.b += str(0)
            self.l.append(bitToDec(self.b))
            self.b = ""

"""
the parser class

represents a byte stream encoded using the stream class. can be used to extract data from the stream


attributes:
    l - type: byte container
    byte container that represents the bytes in the stream

    count - type: string
    represents the position in the stream where data is extracted

functions:
    lPar - input: positive integer | output: positive integer
    takes an amount of bytes n and returns its unsigned integer value

    iPar - no input | output: integer
    reverse algorithm of the lInt method of the stream class

    fPar - no input | output: number
    reverse algorithm of the flo method of the stream class
"""
class parser:
    def __init__(self, l):
        self.l = l
        self.count = 0
        self.bPos = 0
    def lPar(self,n):
        final = int.from_bytes(self.l[self.count:self.count+n],byteorder="big")
        self.count += n
        return final
    def pBit(self, n):
        bs = ""
        for i in range(n):
            if int(self.l[self.count]/pow(2,7-self.bPos))%2:
                bs += "1"
            else:
                bs += "0"
            self.bPos += 1
            if self.bPos == 8:
                self.count += 1
                self.bPos = 0
        return bitToDec(bs)
    def align(self):
        while self.bPos > 0:
            self.pBit(1)
    def iPar(self):
        sLen = self.l[self.count]
        sub = []
        self.count += 1
        for k in range(sLen%128):
            sub.append(self.l[self.count+k])
        self.count += sLen%128
        return parse(sub)*pow(-1,sLen>=128)
    def fPar(self):
        sub5 = self.l[self.count]
        self.count += 1
        isNeg = int(sub5/128)
        isFloat = int(sub5/64)%2
        nLen = sub5%64
        sub6 = 0
        for p in range(nLen):
            sub6 += self.l[self.count]*pow(256,nLen-1-p)
            self.count += 1
        if isFloat:
            sub7 = 0
            for p in range(5):
                sub7 += self.l[self.count]*pow(256,4-p)
                self.count += 1
            sub6 += sub7/pow(2,40)
        return sub6*pow(-1,isNeg)
