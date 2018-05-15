import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

signs = {
    "no_drive": [[119, 101, 73], [255, 255, 255]],
    "stop": [[0, 106, 93], [189, 203, 160]]
}

for i, j in signs.items():
    signs[i] = (j[0], j[1], cv.resize(cv.imread("./signs/{}.png".format(i)), (100, 100)))

while True:
    ret, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    hsv = cv.blur(hsv, (5, 5))

    for s, x in signs.items():
        lower = np.array(x[0])
        upper = np.array(x[1])
        thresh = cv.inRange(hsv, lower, upper)

        thresh = cv.erode(thresh, None, iterations=2)
        thresh = cv.dilate(thresh, None, iterations=4)

        contours = cv.findContours(thresh.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours = contours[1]
        for cnt in contours:
            c = sorted(contours, key=cv.contourArea, reverse=True)[0]
            rect = cv.minAreaRect(c)
            box = np.int0(cv.boxPoints(rect))
            y1 = int(box[0][1])
            x2 = int(box[1][0])
            y2 = int(box[1][1])
            x3 = int(box[2][0])

            roiImg = frame[y2:y1, x2:x3]

            if roiImg.any():
                if abs(len(roiImg) - len(roiImg[0])) > 50 or len(roiImg) < 30 or len(roiImg[0]) < 30:
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
                print(pc, s)
                if pc > 70:
                    cv.drawContours(frame, [box], -1, (0 if s == 'stop' else 255, 255, 0), 3)
                # cv.imshow("test", frame)
                # cv.imshow('roiImg', roiImg)
                # print(identity_percent)

    cv.imshow('frame', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
