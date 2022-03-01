import os
from sys import int_info


class Channel:

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get("name", "can0")
        self.bitrate = kwargs.get("bitrate", 125000)
        self.start()

    def start(self):
        os.system(f'sudo ip link set {self.name} type can bitrate {self.bitrate}')
        os.system(f'sudo ifconfig {self.name} up')

    def stop(self):
        os.system(f'sudo ifconfig {self.name} down')

    def set_bitrate(self, bitrate: int) -> bool:
        if isinstance(bitrate, int):
            self.stop()
            self.bitrate = bitrate
            self.start()
            return True
        return False

    def set_name(self, name: str) -> bool:
        if isinstance(name, str):
            self.stop()
            self.name = name
            self.start()
            return True
        return False
