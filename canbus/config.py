import os
from sys import int_info


class Channel:
    """
    Configuration channels of 2-Channel Isolated CAN Expansion HAT for Raspberry Pi.
    Brand url : https://www.waveshare.com/2-ch-can-hat.htm
    """

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
        """Modifying the channel bitrate
        Args:
            bitrate (int): New bitrate value
        Returns: 
            bool: True if the value has been changed
        """
        if isinstance(bitrate, int):
            self.stop()
            self.bitrate = bitrate
            self.start()
            return True
        return False

    def set_name(self, name: str) -> bool:
        """Modifying the channel name
        Args:
            name (str): Selected channel name
        Returns:
            bool: True if the value has been changed
        """
        if isinstance(name, str):
            self.stop()
            self.name = name
            self.start()
            return True
        return False
