import os
import cv2

if __name__ == '__main__':
    model_num_list = list("4716315746629837143856197283267181943")
    image_path = "model/Sudoku_model.png"
    image = cv2.imread(image_path)  # 读取数独图片

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    # RGB转灰度图
    ret, thresh = cv2.threshold(gray_image, 230, 255, cv2.THRESH_BINARY)    # 阈值分割
    # 对二值图像执行膨胀操作
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (1, 1))
    dilated = cv2.dilate(thresh, kernel)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    for i in range(len(hierarchy[0])):
        if hierarchy[0][i][2] != -1:
            boxes.append(hierarchy[0][i])

    boxes = boxes[::-1]
    for j in range(len(boxes)):
        x, y, w, h = cv2.boundingRect(contours[boxes[j][2]])
        x1 = int(x+w/2-16)
        x2 = int(x+w/2+17)
        y1 = int(y+h/2-24)
        y2 = int(y+h/2+24)
        img = image[y1:y2, x1:x2]
        file_list = os.listdir("model")
        file_name = "model/" + str(model_num_list[j]) + '.png'
        if file_name not in file_list:
            cv2.imwrite(file_name, img)
