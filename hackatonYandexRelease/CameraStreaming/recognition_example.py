import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    hsv = cv.blur(hsv, (5, 5))

    lower = np.array([119, 101, 73])
    upper = np.array([255, 255, 255])
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
            noDrive = cv.imread("./../signs/stop.png")

            resizedRoi = cv.resize(roiImg, (100, 100))
            noDrive = cv.resize(noDrive, (100, 100))

            xresizedRoi = cv.inRange(resizedRoi, lower, upper)
            xnoDrive = cv.inRange(noDrive, lower, upper)

            identity_percent = 0
            for i in range(100):
                for j in range(100):
                    if xresizedRoi[i][j] == xnoDrive[i][j]:
                        identity_percent = identity_percent + 1
            # if identity_percent > 6000:
            cv.drawContours(frame, [box], -1, (0, 255, 0), 3)  # draw contours in green color
            # cv.imshow("test", frame)
            # cv.imshow('roiImg', roiImg)
            print(identity_percent)

    cv.imshow('frame', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
