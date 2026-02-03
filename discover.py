import json
from os import PathLike
from onvif import ONVIFDiscovery
from onvif import ONVIFClient
import subprocess

class DeviceDiscoverer:
    def __init__(self, credentials_path: str|PathLike):
        self.credentials = {}
        with open(credentials_path, "r") as f:
            self.credentials = json.load(f)['credentials']

    def start_discover(self) -> ONVIFClient:
        print("Turning of Wi-Fi temporarily")
        subprocess.run(["sudo", "ip", "link", "set", "wlan0", "down"], check=True)

        print("Discovering ONVIF devices...")
        while True:
            discovery = ONVIFDiscovery(timeout=5, interface="eth0")
            print(f"Discovering devices on {discovery.interface}")
            devices = discovery.discover()
            print("Could not find any devices. Trying again...")

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

        subprocess.run(["sudo", "ip", "link", "set", "wlan0", "up"], check=True)

        return client
