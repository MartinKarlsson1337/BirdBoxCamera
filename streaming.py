import cv2
import threading
import queue
from typing import List
from abc import ABC, abstractmethod

class PipelineComponent(threading.Thread, ABC):
    def __init__(self):
        super().__init__()
        self.input_buffer = None
        self.output_buffer = None
        self.should_stop = False

    def stop_running(self):
        self.should_stop = True

    def connect_input_buffer(self, input_buffer: queue.Queue):
        self.input_buffer = input_buffer

    def connect_output_buffer(self, output_buffer: queue.Queue):
        self.output_buffer = output_buffer

    @abstractmethod
    def component_function(self):
        print("Run has not been implemented")

    def run(self):
        while self.should_stop:
            self.component_function()


class Pipeline():
    def __init__(self, components: List[PipelineComponent], default_buffer_size: int = 10):
        self.components = components
        self.default_buffer_size = default_buffer_size
        self.buffers = []

        for idx, component in enumerate(self.components):
            if idx == 0:
                input_buffer = queue.Queue(self.default_buffer_size)
                output_buffer = queue.Queue(self.default_buffer_size)

            else:
                input_buffer = self.components[idx - 1].output_buffer
                output_buffer = queue.Queue(self.default_buffer_size)

            component.connect_input_buffer(input_buffer)
            component.connect_output_buffer(output_buffer)
            
            self.buffers.append(input_buffer)
            self.buffers.append(output_buffer)
            
    def get_final_output_buffer(self) -> queue.Queue:
        return self.buffers[-1]

    def stop_pipeline(self):
        for component in self.components:
            component.stop_running()
            component.join()

    def start_pipeline(self):
        for component in self.components:
            component.start()
        

class FrameEncoder(PipelineComponent):
    def __init__(self):
        super().__init__()

    def component_function(self):
        frame = self.input_buffer.get()
        print("Encoder: Got next frame to encode")
        imgencode = cv2.imencode('.jpg', frame)[1]
        stringData = imgencode.tobytes()
        output = (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        print("Encoder: Finished encoding. Enqueueing frame")
        self.output_buffer.put(output)


class RTSPStreamer(PipelineComponent):
    def __init__(self, stream_url: str):
        super().__init__()
        self.rtsp_url = stream_url
        print("RTSP client: Starting streaming")
        self.capture = cv2.VideoCapture(self.rtsp_url)
        print("RTSP client: Stream started")

    def stop_running(self):
        self.capture.release()
        return super().stop_running()

    def component_function(self):
        if not self.capture.isOpened():
            print("Error: Cannot open the RTSP stream.")
            exit()

            ret, frame = capture.read()
            if not ret:
                print("Error: Cannot grab frame from RTSP stream.")

            print("RTSP client: Enqueued next frame")
            self.output_buffer.put(frame)
