import time
import can


class CanBus:

    def __init__(self, *args, **kwargs):
        self.bus = can.Bus(channel=kwargs.get('channel', 'can0'), interface='socketcan')

    def send_messages(self, id:int, msg_list: list, is_extended_id: bool, delay=0.3):
        for msg in msg_list:
            if not isinstance(msg, list):
                msg_send = can.Message(arbitration_id=id, data=msg_list, is_extended_id=is_extended_id)
                self.bus.send(msg_send)
                break
            else:
                msg_send = can.Message(arbitration_id=id, data=msg, is_extended_id=is_extended_id)
                self.bus.send(msg_send)
                time.sleep(delay)
            
    
    def recv(self, *args, **kwargs):
        return self.bus.recv(*args, **kwargs)

    @staticmethod
    def data_print(msg):
        try:
            print(f"ID: 0x{msg.arbitration_id:02X} - data: {' '.join([f'{a:02X}' for a in msg.data])}")
        except AttributeError:
            pass
