import cv2
import numpy as np


def generate_list(num_list, file_name, flag=0):
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
        hang = int(x_center // (690//9))
        lie = int(y_center // (695//9))
        ls[lie][hang] = int(num_list[j])
    return ls
