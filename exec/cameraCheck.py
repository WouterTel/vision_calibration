import cv2

cap = cv2.VideoCapture('rtsp://user1:Dymat0!1!@192.168.0.64:554/profile2/media.smp', cv2.CAP_FFMPEG)
while True:
    ret, frame = cap.read()
    if ret == False:
        print('Nope')
        break
    else:
        cv2.imshow('video',frame)
        cv2.waitKey(0)