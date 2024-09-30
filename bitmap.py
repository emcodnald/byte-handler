"""
bitmap handling module
"""

"""
the matrix function - input: string | output: three dimensional matrix
takes a filename, opens the file, and converts the contents into a matrix representing the pixel data
"""
def matrix(fn):
    with open(fn, 'rb') as f:
        a = f.read()
    f.close()
    width = a[19]*256+a[18]
    height = a[23]*256+a[22]
    pW = (len(a)-54)/height
    final = []
    for i in range(height):
        final.append([])
        for j in range(width):
            sub = []
            for k in range(3):
                sub.append(a[54+(height-i-1)*int(pW)+j*3+2-k])
            final[i].append(sub)
    return final

"""
the image function - input: three dimensional matrix | no output
takes a three dimensional pixel matrix and converts it into a .bmp image
"""
def image(ma,fn):
    with open(fn, 'wb') as f:
        startBytes = [66, 77, 110, 87, 7, 0, 0, 0, 0, 0, 54, 0, 0, 0, 40, 0, 0, 0, len(ma[0])%256, int(len(ma[0])/256)%256, int(len(ma[0])/65536)%256, int(len(ma[0])/16777216)%256, len(ma)%256, int(len(ma)/256)%256, int(len(ma)/65536)%256, int(len(ma)/16777216)%256, 1, 0, 24, 0, 0, 0, 0, 0, 56, 87, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(startBytes)):
            f.write(startBytes[i].to_bytes(1,byteorder="big"))
        for i in range(len(ma)-1,-1,-1):
            for j in range(len(ma[i])):
                for k in range(3):
                    f.write((ma[i][j][2-k]).to_bytes(1,byteorder="big"))
            for j in range(len(ma[i])%4):
                f.write((0).to_bytes(1, byteorder='big'))
    f.close()
