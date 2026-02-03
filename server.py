from flask import Flask, render_template, Response
from camera_manager import CameraManager

app = Flask(__name__)

camera_manager = CameraManager()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video')
def video():
    return Response(camera_manager.streamer.start_streaming(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(threaded=True, host="0.0.0.0", port=5000)