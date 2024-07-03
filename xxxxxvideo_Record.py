import cv2

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# the other formate: XVID => avi

vw = cv2.VideoWriter('output.mp4',fourcc,20,(640,480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print('can not recive frame, Exiting...')
        break

    vw.write(frame)
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()

# 释放VideoWriter
vw.release()

cv2.destroyAllWindows()