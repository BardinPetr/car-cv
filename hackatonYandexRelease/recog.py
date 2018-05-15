import numpy as np
import cv2 as cv
import socket

cap = cv.VideoCapture(0)

signs = {
    "no_drive": [[0, 173, 0], [60, 255, 255]],  # [[119, 101, 73], [255, 255, 255]],
    #"stop": [[0, 173, 0], [60, 255, 255]],
    #"a_unevenness": [[0, 173, 0], [60, 255, 255]],
    "main_road": [[0, 115, 96], [29, 161, 189]],
    #"no_entry": [[0, 173, 0], [60, 255, 255]],
    "parking": [[97, 107, 130], [145, 255, 255]],
    "pedistrain": [[107, 183, 92], [153, 135, 122]],
    "road_works": [[26, 79, 132], [46, 174, 255]]
    #"way_out": [[0, 173, 0], [60, 255, 255]]
}
'''
def get_colors(x):
    res = {
        'red': 0,
        'blue': 0,
        'yellow': 0,
        'black': 0
    }
    
'''
for i, j in signs.items():
    a = cv.resize(cv.imread("./signs/{}.png".format(i)), (100, 100))
    signs[i] = (j[0], j[1], a)


def dist(h0, h1):
    return min(abs(h1 - h0), 360 - abs(h1 - h0))


fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output.avi', fourcc, 30.0, (640, 480))

sk = socket.socket()
sk.connect(('172.24.1.98', 1092))

ct = 0
while True:
    result = set()
    ret, frame = cap.read()
    ct += 1
    if ct % 3 == 0:
        ct = 0
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        hsv = cv.blur(hsv, (5, 5))
        f = True
        for s, x in signs.items():
            if not f:
                break
            lower = np.array(x[0])
            upper = np.array(x[1])
            thresh = cv.inRange(hsv, lower, upper)

            thresh = cv.erode(thresh, None, iterations=2)
            thresh = cv.dilate(thresh, None, iterations=4)
            #cv.imshow('t', thresh)
            contours = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            contours = contours[1]
            for cnt in contours:
                if not f:
                    break
                c = sorted(contours, key=cv.contourArea, reverse=True)[0]
                rect = cv.minAreaRect(c)
                box = np.int0(cv.boxPoints(rect))
                y1 = int(box[0][1])
                x2 = int(box[1][0])
                y2 = int(box[1][1])
                x3 = int(box[2][0])

                roiImg = frame[y2:y1, x2:x3]

                if roiImg.any():
                    if abs(len(roiImg) - len(roiImg[0])) > 50 or len(roiImg) < 50 or len(roiImg[0]) < 50:
                        continue
                    noDrive = x[2]
                    resizedRoi = cv.resize(roiImg, (100, 100))
                    xresizedRoi = cv.inRange(resizedRoi, lower, upper)
                    xnoDrive = cv.inRange(noDrive, lower, upper)

                    identity_percent = 0
                    for i in range(100):
                        for j in range(100):
                            if xresizedRoi[i][j] == xnoDrive[i][j]:
                                identity_percent = identity_percent + 1
                    pc = identity_percent / 10000 * 100
                    if 60 < pc < 101:
                        cv.drawContours(frame, [box], -1, (0, 0, 255), 3)
                        cv.putText(frame, s, (box[0][0], box[0][1]), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        result.add(s)
                        f = False
                        break

                    # cv.imshow("test", frame)
                    # cv.imshow('roiImg', roiImg)
                    # print(identity_percent)

        #cv.imshow('frame', frame)
        out.write(frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        sk.send(','.join(list(result)).encode('utf-8'))

sk.close()
cap.release()
cv.destroyAllWindows()
