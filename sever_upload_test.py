import cv2
import mediapipe as mp
import time
import requests
import numpy as np

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils
handLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=3)
handConStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=5)
pTime = 0
cTime = 0

while True:
    ret, img = cap.read()
    if ret:
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(imgRGB)

        imgHeight = img.shape[0]
        imgWidth = img.shape[1]

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConStyle)
                for i, lm in enumerate(handLms.landmark):
                    xPos = int(lm.x * imgWidth)
                    yPos = int(lm.y * imgHeight)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, f"FPS : {int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

        # 将图像编码为JPEG格式
        _, img_encoded = cv2.imencode('.jpg', img)
        # 将图像作为文件发送到Flask服务器
        files = {'file': ('image.jpg', img_encoded.tobytes(), 'image/jpeg')}
        response = requests.post("http://127.0.0.1:5000/upload", files=files)
        print(response.json())

        # 从服务器获取最新的图像
        img_response = requests.get("http://127.0.0.1:5000/latest_image")
        if img_response.status_code == 200:
            nparr = np.frombuffer(img_response.content, np.uint8)
            img_from_server = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imshow('Latest Uploaded Image', img_from_server)
        else:
            print('No image available on server')

        cv2.imshow('img', img)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
