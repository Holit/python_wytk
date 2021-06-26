import cv2
import numpy
import pylab
import matplotlib.pyplot as plt
import math
import struct
import array
import sys
import time

starttime = time.time()

argv = sys.argv
if(len(argv) != 2):
    print("用法: dewytk [filename]")
    print("将在执行路径生成图片")
    endtime = time.time()
    print('[!-1]耗时', str(round(endtime - starttime, 2)),'秒')
    exit(-1)
else:
    imgfile = argv[1]

try:
    img = cv2.imread(imgfile,cv2.IMREAD_UNCHANGED)
    imgdata = []
    rawdata = dict()
    
    #print("图像的形状,返回一个图像的(行数,列数,通道数):",img.shape)
    
    n = img.size
    
    a = 1
    mode = 4
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            p = img[i][j]
            #BGRA
            rawdata = dict()
            rawdata['R'] = p[0]
            rawdata['G'] = p[1]
            rawdata['B'] = p[2]
            imgdata.append(rawdata)
            if(i == 0 and j == 0):
                mode = p[0] % 8
                if ( mode <= 0 or mode >4):

                    endtime = time.time()
                    print('[!-3]耗时', str(round(endtime - starttime, 2)),'秒')
                    exit(-3)
    
    aa = math.ceil(3*mode/8)
    n = img.size
    j = 0
    k = ""
    current_pixel_index = 1
    word = ""
    blist = []
    blength = 0
    while(current_pixel_index < n and (len(word) == 0 or ord(word[-1])>0 )):
        k = k+str(bin(imgdata[current_pixel_index]['B'] + 256))[-mode:]
        k = k+str(bin(imgdata[current_pixel_index]['G'] + 256))[-mode:]
        k = k+str(bin(imgdata[current_pixel_index]['R'] + 256))[-mode:]
        current_pixel_index = current_pixel_index +1
        for i in range(0,aa):
            if(len(k) >= 8 and (len(word) == 0 or ord(word[-1]) > 0)):
                word = word + chr(int(k[0:8],2))
                k = k[8:]
    #ref to lines#139
    blength = int(word.split(chr(1))[0])
    if(blength <= -1 or not (len(word.split(chr(1))) >2)):
        endtime = time.time()
        print('[!-2]无法处理未知的隐写参数。耗时', str(round(endtime - starttime, 2)),'秒')
        exit(-2)
    blist = []
    
    if(len(k) >= 8 and j < blength):
        blist.append(int(k[0:8],2))
        k = k[8:]
        j = j + 1
    while (current_pixel_index < n and j < blength):
        k = k+str(bin(imgdata[current_pixel_index]['B'] + 256))[-mode:]
        k = k+str(bin(imgdata[current_pixel_index]['G'] + 256))[-mode:]
        k = k+str(bin(imgdata[current_pixel_index]['R'] + 256))[-mode:]
        current_pixel_index = current_pixel_index +1
        for i in range(0,aa):
            if(len(k) >= 8 and j<blength):
                blist.append(int(k[0:8],2))
                k = k[8:]
                j = j + 1
    
    
    with open(str(word.split(chr(1))[1]), 'wb')as fp:
        for x in blist:
            a = struct.pack('B', x)
            fp.write(a)
    endtime = time.time()
    print("已经向源文件 " + str(word.split(chr(1))[1]) + "\t写入了 " + str(word.split(chr(1))[0]) + "\t字节,耗时 " + str(round(endtime - starttime, 2))+ "\t秒")
    exit(0)
    pass
except:
    endtime = time.time()
    print("[!-5]" + '耗时', str(round(endtime - starttime, 2)),'秒')
    exit(-5)
    pass
