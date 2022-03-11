import time
import can


class CanBus:

    def __init__(self, *args, **kwargs):
        self.bus = can.Bus(channel=kwargs.get('channel', 'can0'), interface='socketcan')

    def send_messages(self, id:int, msg_list: list, delay=0.3):

        for msg in msg_list:
            if not isinstance(msg, list):
                msg_send = can.Message(arbitration_id=id, data=msg_list, is_extended_id=self._is_extended(id))
                self.bus.send(msg_send)
                break
            else:
                msg_send = can.Message(arbitration_id=id, data=msg, is_extended_id=self._is_extended(id))
                self.bus.send(msg_send)
            time.sleep(delay)
            
    
    def recv(self, *args, **kwargs):
        return self.bus.recv(*args, **kwargs)

    def _decode(self, data):
        try:
            return data.decode().strip()
        except UnicodeDecodeError:
            return None

    @staticmethod
    def data_print(msg):
        try:
            print(f"ID: 0x{msg.arbitration_id:02X} - data: {' '.join([f'{a:02X}' for a in msg.data])}")
        except AttributeError:
            pass

    @staticmethod
    def _is_extended(id):
        if id >= 0xFFF:
            return True
        return False
