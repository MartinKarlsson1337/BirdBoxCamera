from onvif import ONVIFClient
from onvif.client import Media, Media2
from streaming import RTSPStreamer
from discover import DeviceDiscoverer

class CameraManager:
    def __init__(self):
        # Discover ONVIF devices
        discoverer = DeviceDiscoverer("secrets.json")
        #self.client: ONVIFClient = discoverer.start_discover()
        self.client: ONVIFClient = discoverer.connect_directly("192.168.1.43", 80)
        self.media = self.client.media()
        self.media2 = self.client.media2()

        # Remove On screen displays (Camera has timestamp by default)
        self._clear_osds()

        # Find video stream
        stream_uri = self._get_stream()

        # Start streaming
        self.streamer = RTSPStreamer(stream_uri["Uri"])

    def _clear_osds(self):
        osds = self.media2.GetOSDs()
        for osd in osds:
            self.media2.DeleteOSD(osd.token)

    def _get_stream(self):
        profiles = self.media.GetProfiles()
        main_stream = None
        for profile in profiles:
            if profile['Name'] == 'MainStream':
                main_stream = profile

        profile_token = main_stream['token']
        stream_setup = {"Stream": "RTP-Unicast", "Transport": {"Protocol": "UDP"}}
        stream_uri = self.media.GetStreamUri(StreamSetup=stream_setup, ProfileToken=profile_token)
        return stream_uri


