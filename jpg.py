"""
.jpg image handling module
"""

import math
def alp(n):
    if n == 0:
        return 1/math.sqrt(2)
    else:
        return 1
def dct(m):
    final = []
    for v in range(8):
        final.append([])
        for u in range(8):
            sub = 0
            for i in range(8):
                for j in range(8):
                    sub += m[i][j]*math.cos((2*j+1)*u*math.pi/16)*math.cos((2*i+1)*v*math.pi/16)
            final[v].append(round(sub*alp(u)*alp(v)/4))
    return final
def conv(a):
    return [0.299*a[0]+0.587*a[1]+0.114*a[2],128-0.168736*a[0]-0.331264*a[1]+0.5*a[2],128+0.5*a[0]-0.418688*a[1]-0.081312*a[2]]
def decToBit(num):
    finalString = ""
    l = int(math.log(abs(num),2)+1)
    for i in range(l):
        if num >= 0:
            finalString += str(math.floor(num/pow(2,(l-1)-i)%2))
        else:
            if math.floor(abs(num)/pow(2,(l-1)-i)%2) == 0:
                finalString += "1"
            else:
                finalString += "0"
    return finalString
def showBitsL(num,l):
    finalString = ""
    for i in range(l):
        finalString += str(math.floor(num/pow(2,(l-1)-i)%2))
    return finalString
def bitToDec(s):
    final = 0
    for i in range(8):
        if s[i] == "1":
            final += pow(2,7-i)
    return final

"""
the image function - input: three dimensional matrix, string, integer ranged 1 - 255 | no output
takes a three dimensional pixel matrix and converts it into a .jpg image using constant quantization, with 1 being the least lossy and 255 being the most lossy
"""
def image(ma,fn,qt):
    b = [[255, 216], [255, 224, 0, 16, 74, 70, 73, 70, 0, 1, 1, 1, 0, 96, 0, 96, 0, 0], [255, 225, 0, 34, 69, 120, 105, 102, 0, 0, 77, 77, 0, 42, 0, 0, 0, 8, 0, 1, 1, 18, 0, 3, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0], [255, 219, 0, 67, 0], [255, 219, 0, 67, 1], [255, 192, 0, 17, 8, 0, 0, 0, 0, 3, 1, 34, 0, 2, 17, 1, 3, 17, 1], [255, 196, 0, 31, 0, 0, 1, 5, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [255, 196, 0, 181, 16, 0, 2, 1, 3, 3, 2, 4, 3, 5, 5, 4, 4, 0, 0, 1, 125, 1, 2, 3, 0, 4, 17, 5, 18, 33, 49, 65, 6, 19, 81, 97, 7, 34, 113, 20, 50, 129, 145, 161, 8, 35, 66, 177, 193, 21, 82, 209, 240, 36, 51, 98, 114, 130, 9, 10, 22, 23, 24, 25, 26, 37, 38, 39, 40, 41, 42, 52, 53, 54, 55, 56, 57, 58, 67, 68, 69, 70, 71, 72, 73, 74, 83, 84, 85, 86, 87, 88, 89, 90, 99, 100, 101, 102, 103, 104, 105, 106, 115, 116, 117, 118, 119, 120, 121, 122, 131, 132, 133, 134, 135, 136, 137, 138, 146, 147, 148, 149, 150, 151, 152, 153, 154, 162, 163, 164, 165, 166, 167, 168, 169, 170, 178, 179, 180, 181, 182, 183, 184, 185, 186, 194, 195, 196, 197, 198, 199, 200, 201, 202, 210, 211, 212, 213, 214, 215, 216, 217, 218, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250], [255, 196, 0, 31, 1, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [255, 196, 0, 181, 17, 0, 2, 1, 2, 4, 4, 3, 4, 7, 5, 4, 4, 0, 1, 2, 119, 0, 1, 2, 3, 17, 4, 5, 33, 49, 6, 18, 65, 81, 7, 97, 113, 19, 34, 50, 129, 8, 20, 66, 145, 161, 177, 193, 9, 35, 51, 82, 240, 21, 98, 114, 209, 10, 22, 36, 52, 225, 37, 241, 23, 24, 25, 26, 38, 39, 40, 41, 42, 53, 54, 55, 56, 57, 58, 67, 68, 69, 70, 71, 72, 73, 74, 83, 84, 85, 86, 87, 88, 89, 90, 99, 100, 101, 102, 103, 104, 105, 106, 115, 116, 117, 118, 119, 120, 121, 122, 130, 131, 132, 133, 134, 135, 136, 137, 138, 146, 147, 148, 149, 150, 151, 152, 153, 154, 162, 163, 164, 165, 166, 167, 168, 169, 170, 178, 179, 180, 181, 182, 183, 184, 185, 186, 194, 195, 196, 197, 198, 199, 200, 201, 202, 210, 211, 212, 213, 214, 215, 216, 217, 218, 226, 227, 228, 229, 230, 231, 232, 233, 234, 242, 243, 244, 245, 246, 247, 248, 249, 250], [255, 218, 0, 12, 3, 1, 0, 2, 17, 3, 17, 0, 63, 0], [255, 217]]
    hTables = []
    for i in range(6,10):
        hTables.append([[],[]])
        for j in range(5,21):
            hTables[-1][0].append(b[i][j])
        for j in range(21,len(b[i])):
            hTables[-1][1].append(b[i][j])
    hCodes = []
    for k in range(4):
        hCodes.append([])
        e = 0
        off = 0
        for i in range(len(hTables[k][0])):
            for j in range(hTables[k][0][i]):
                hCodes[-1].append([hTables[k][1][off+j],showBitsL(e,i+1)])
                e += 1
            off += hTables[k][0][i]
            e *= 2
    ybr = []
    for i in range(len(ma)):
        ybr.append([])
        for j in range(len(ma[i])):
            sub = []
            for k in range(3):
                sub.append(ma[i][j][k])
            samp = conv(sub)
            ybr[-1].append(samp)
    width = len(ma[0])
    height = len(ma)
    rX = math.ceil(width/16)
    rY = math.ceil(height/16)
    runs = rX*rY
    bitStr = ""
    pConst = []
    pConst2 = []
    pConst3 = []
    for x in range(runs):
        y = []
        doit = False
        for i in range(4):
            y.append([])
            for j in range(8):
                y[i].append([])
                for k in range(8):
                    sampX = k+(i%2)*8+(x%rX)*16
                    sampY = int(i/2)*8+j+int(x/rX)*16
                    if sampY >= height:
                        sampY = -1
                    if sampX >= width:
                        sampX = -1
                    y[i][j].append(ybr[sampY][sampX][0])
        cb = []
        r = []
        for i in range(8):
            cb.append([])
            r.append([])
            for j in range(8):
                ab = 0
                ar = 0
                for k in range(2):
                    for m in range(2):
                        sampX = j*2+m+(x%rX)*16
                        sampY = i*2+k+16*int(x/rX)
                        if sampY >= height:
                            sampY = -1
                        if sampX >= width:
                            sampX = -1
                        ab += ybr[sampY][sampX][1]/4
                        ar += ybr[sampY][sampX][2]/4
                cb[i].append(ab)
                r[i].append(ar)
        mList=[y[0],y[1],y[2],y[3],cb,r]
        e = ""
        for z in range(len(mList)):
            s = mList[z]
            for i in range(8):
                for j in range(8):
                    s[i][j] -= 128
            g = dct(s)
            for i in range(8):
                for j in range(8):
                    g[i][j] = round(g[i][j]/qt)
            ec = []
            count = 0
            while count < 15:
                count2 = abs(7-abs(7-count))
                while count2 >= 0:
                    if count < 8:
                        if count%2 == 0:
                            ind = [count2,abs(7-abs(7-count))-count2]
                        else:
                            ind = [abs(7-abs(7-count))-count2,count2]
                    else:
                        if count%2 == 0:
                            ind = [count2+7-abs(7-abs(7-count)),7-count2]
                        else:
                            ind = [7-count2,count2+7-abs(7-abs(7-count))]
                    ec.append(g[ind[0]][ind[1]])
                    count2 -= 1
                count += 1
            count = -1
            while ec[count] == 0 and count > -len(ec):
                count -= 1
            count += 65
            ec[count:len(ec)] = []
            bitPairs = []
            if z > 3:
                if z == 4:
                    if len(pConst2) == 0:
                        if not ec[0] == 0:
                            bitPairs.append([int(math.log(abs(ec[0]),2)+1),ec[0]])
                        else:
                            bitPairs.append([0,0])
                    else:
                        if not ec[0]-pConst2[-1] == 0:
                            bitPairs.append([int(math.log(abs(ec[0]-pConst2[-1]),2)+1),ec[0]-pConst2[-1]])
                        else:
                            bitPairs.append([0,0])
                    pConst2.append(ec[0])
                elif z == 5:
                    if len(pConst3) == 0:
                        if not ec[0] == 0:
                            bitPairs.append([int(math.log(abs(ec[0]),2)+1),ec[0]])
                        else:
                            bitPairs.append([0,0])
                    else:
                        if not ec[0]-pConst3[-1] == 0:
                            bitPairs.append([int(math.log(abs(ec[0]-pConst3[-1]),2)+1),ec[0]-pConst3[-1]])
                        else:
                            bitPairs.append([0,0])
                    pConst3.append(ec[0])
            else:
                if len(pConst) > 0:
                    if not ec[0]-pConst[-1] == 0:
                        bitPairs.append([int(math.log(abs(ec[0]-pConst[-1]),2)+1),ec[0]-pConst[-1]])
                    else:
                        bitPairs.append([0,0])
                else:
                    if not ec[0] == 0:
                        bitPairs.append([int(math.log(abs(ec[0]),2)+1),ec[0]])
                    else:
                        bitPairs.append([0,0])
                pConst.append(ec[0])
            prez = 0
            for i in range(1,len(ec)):
                if not ec[i] == 0:
                    while prez >= 16:
                        bitPairs.append([240,0])
                        prez -= 16
                    bitPairs.append([int(math.log(abs(ec[i]),2)+1)+prez*16,ec[i]])
                    prez = 0
                else:
                    prez += 1
            if len(ec) < 64:
                bitPairs.append([0,0])
            for i in range(len(bitPairs)):
                if z < 4:
                    if i == 0:
                        bitStr += hCodes[0][bitPairs[i][0]][1]
                        if not bitPairs[i][1] == 0:
                            bitStr += decToBit(bitPairs[i][1])
                    else:
                        for j in range(len(hCodes[1])):
                            if hCodes[1][j][0] == bitPairs[i][0]:
                                bitStr += hCodes[1][j][1]
                                if not bitPairs[i][1] == 0:
                                    bitStr += decToBit(bitPairs[i][1])
                else:
                    if i == 0:
                        bitStr += hCodes[2][bitPairs[i][0]][1]
                        if not bitPairs[i][1] == 0:
                            bitStr += decToBit(bitPairs[i][1])
                    else:
                        for j in range(len(hCodes[3])):
                            if hCodes[3][j][0] == bitPairs[i][0]:
                                bitStr += hCodes[3][j][1]
                                if not bitPairs[i][1] == 0:
                                    bitStr += decToBit(bitPairs[i][1])
    while not len(bitStr)%8 == 0:
        bitStr += "1"
    e = bitStr
    d = []
    sample = ""
    for i in range(len(e)):
        sample += e[i]
        if len(sample) == 8:
            d.append(bitToDec(sample))
            if d[-1] == 255:
                d.append(0)
            sample = ""
    for i in range(len(d)):
        b[-2].append(d[i])
    b[5][5] = int(height/256)
    b[5][6] = height%256
    b[5][7] = int(width/256)
    b[5][8] = width%256
    for i in range(64):
        b[3].append(qt)
        b[4].append(qt)
    with open(fn, 'wb') as f:
        for i in range(len(b)):
            for j in range(len(b[i])):
                f.write((b[i][j]).to_bytes(1, byteorder='big'))
