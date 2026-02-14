import cv2
import threading
import queue
from typing import List
from abc import ABC, abstractmethod

class PipelineComponent(threading.Thread, ABC):
    def __init__(self, input_buffer: queue.Queue, output_buffer: queue.Queue):
        super.__init__(self)
        self.input_buffer = input_buffer
        self.output_buffer = output_buffer
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
        super.__init__(self)

    def component_function(self):
        frame = self.input_buffer.get()
        imgencode = cv2.imencode('.jpg', frame)[1]
        stringData = imgencode.tobytes()
        output = (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')
        self.output_buffer.put(output)


class RTSPStreamer(PipelineComponent):
    def __init__(self, stream_url: str):
        super.__init__(self)
        self.rtsp_url = stream_url
        self.capture = cv2.VideoCapture(self.rtsp_url)

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

            self.output_buffer.put(frame)
