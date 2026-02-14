from flask import Flask, render_template, Response
from camera_manager import CameraManager
from streaming import Pipeline, RTSPStreamer, FrameEncoder
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='server.log', encoding='utf-8', level=logging.DEBUG)

app = Flask(__name__)

camera_manager = CameraManager()
stream_uri = camera_manager.get_stream()['Uri']
pipeline = Pipeline([
    RTSPStreamer(stream_uri),
    FrameEncoder()
])
output_buffer = pipeline.get_final_output_buffer()


def frame_getter():
    while True:
        logger.info("Frame getter: Waiting for next frame...")
        output = output_buffer.get()
        logger.info("Frame getter: Got next frame. Yielding...")
        yield output


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/video')
def video():
    return Response(frame_getter(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    pipeline.start_pipeline()
    app.run(threaded=True, host="0.0.0.0", port=5000)
    pipeline.stop_pipeline()