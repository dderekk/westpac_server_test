import cv2
import time
import requests

def capture_video(duration, output_path):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return False

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (640, 480))

    start_time = time.time()
    while int(time.time() - start_time) < duration:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not grab a frame.")
            break
        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return True

def upload_video(url, video_path):
    with open(video_path, 'rb') as f:
        files = {'file': (video_path, f, 'video/mp4')}
        response = requests.post(url, files=files)
        return response.json()

if __name__ == "__main__":
    url = 'http://192.168.56.1:5000/upload'
    video_path = 'captured_video.mp4'
    duration = 10  # Capture duration in seconds

    while True:
        print("Capturing video...")
        if capture_video(duration, video_path):
            print("Uploading video...")
            response = upload_video(url, video_path)
            print("Server response:", response)
        time.sleep(10)  # Wait 10 seconds before capturing the next video
