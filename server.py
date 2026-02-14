from flask import Flask, render_template, Response
from camera_manager import CameraManager
from streaming import Pipeline, RTSPStreamer, FrameEncoder


app = Flask(__name__)

camera_manager = CameraManager()
stream_uri = camera_manager.get_stream()
pipeline = Pipeline([
    RTSPStreamer(stream_uri),
    FrameEncoder()
])
output_buffer = pipeline.get_final_output_buffer()


def frame_getter():
    while True:
        yield output_buffer.get()


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video')
def video():
    return Response(frame_getter(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(threaded=True, host="0.0.0.0", port=5000)