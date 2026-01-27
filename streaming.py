import cv2
import threading

class RTSPStreamer:
    def __init__(self, stream_url: str):
        self.rtsp_url = stream_url

    def start_streaming(self):
        capture = cv2.VideoCapture(self.rtsp_url)

        if not capture.isOpened():
            print("Error: Cannot open the RTSP stream.")
            exit()

        while True:
            # Read a frame
            ret, frame = capture.read()
            if not ret:
                print("Error: Cannot grab frame from RTSP stream.")
                break

            imgencode = cv2.imencode('.jpg', frame)[1]
            stringData = imgencode.tobytes()
            yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

        capture.release()
