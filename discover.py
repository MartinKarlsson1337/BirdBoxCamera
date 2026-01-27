import json
from os import PathLike
from onvif import ONVIFDiscovery
from onvif import ONVIFClient

class DeviceDiscoverer:
    def __init__(self, credentials_path: str|PathLike):
        self.credentials = {}
        with open(credentials_path, "r") as f:
            self.credentials = json.load(f)['credentials']

    def start_discover(self) -> ONVIFClient:
        while True:
            discovery = ONVIFDiscovery(timeout=5)
            devices = discovery.discover()

            if len(devices) > 0:
                break

        camera_host = ""
        camera_port = 0

        for device in devices:
            print(f"Found device at {device['host']}:{device['port']}")
            camera_host = device['host']
            camera_port = device['port']

        client = ONVIFClient(
            host=camera_host,
            port=camera_port,
            username=self.credentials['username'],
            password=self.credentials['password']
        )

        return client
