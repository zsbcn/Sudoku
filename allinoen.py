import time

import cv2
import numpy as np


def dHash(img):
    # 差值哈希算法
    # 缩放8*8
    img = cv2.resize(img, (9, 8))
    # 转换灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hash_str = ''
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(8):
        for j in range(8):
            if gray[i, j] > gray[i, j+1]:
                hash_str = hash_str+'1'
            else:
                hash_str = hash_str+'0'
    return hash_str


def cmpHash(hash1, hash2):
    # Hash值对比
    # 算法中1和0顺序组合起来的即是图片的指纹hash。顺序不固定，但是比较的时候必须是相同的顺序。
    # 对比两幅图的指纹，计算汉明距离，即两个64位的hash值有多少是不一样的，不同的位数越小，图片越相似
    # 汉明距离：一组二进制数据变成另一组数据所需要的步骤，可以衡量两图的差异，汉明距离越小，则相似度越高。汉明距离为0，即两张图片完全一样
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1) != len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 不相等则n计数+1，n最终为相似度
        if hash1[i] != hash2[i]:
            n = n + 1
    return n


def generate_list_in_one(file_name):
    board_num_list = []
    array = np.ones((9, 9)) * 0
    ls = array.astype(int).tolist()
    image = cv2.imread(file_name)  # 读取数独图片

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    # RGB转灰度图
    ret, thresh = cv2.threshold(gray_image, 230, 255, cv2.THRESH_BINARY)    # 阈值分割

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    for i in range(len(hierarchy[0])):
        if hierarchy[0][i][2] != -1:
            boxes.append(hierarchy[0][i])

    boxes = boxes[::-1]
    for j in range(len(boxes)):
        x, y, w, h = cv2.boundingRect(contours[boxes[j][2]])
        x_center = (x + w // 2)
        y_center = (y + h // 2)
        x1 = int(x + w / 2 - 16)
        x2 = int(x + w / 2 + 17)
        y1 = int(y + h / 2 - 24)
        y2 = int(y + h / 2 + 24)
        img = image[y1:y2, x1:x2]
        target = 0
        best = 64
        for i in range(1, 10):
            template = cv2.imread('model/' + str(i) + '.png')
            hash1 = dHash(img)
            hash2 = dHash(template)
            n2 = cmpHash(hash1, hash2)
            if n2 < best:
                best = n2
                target = i
        print(target, n2)
        board_num_list.append(target)
        hang = int(x_center // (690//9))
        lie = int(y_center // (695//9))
        ls[lie][hang] = target
    return ls
