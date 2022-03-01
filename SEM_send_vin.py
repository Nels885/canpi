import time
import can
from binascii import hexlify

from canbus import data_print
from canbus.config import Channel
from constances import CAN_CFG

BITRATE_125 = 125000
BITRATE_250 = 250000
BITRATE_500 = 500000

sem = CAN_CFG.get("SEM")
ID_DIAG = sem.get("ID_DIAG")
ID_REPLY = sem.get("ID_REPLY")
app_soft = sem.get('ApplicationSoftwareIdentificationDataIdentifier')


def main():
    bus = can.Bus(channel='can1', interface='socketcan')# socketcan

    while True:
        msg = bus.recv()
        data_print(msg)

        if msg.arbitration_id == ID_DIAG and msg.data == bytearray(app_soft):
            print("OK => ApplicationSoftwareIdentificationDataIdentifer")
            msg_list = [
                [0x10, 0x10, 0x62, 0xF1, 0x81, 0x01, 0x05, 0x32],
                [0x21, 0x32, 0x36, 0x36, 0x39, 0x34, 0x37, 0x36],
                [0x22, 0x43, 0x30, 0x31, 0x00, 0x00, 0x00, 0x00]
            ]
            for msg in msg_list:
                msg_send = can.Message(arbitration_id=ID_REPLY, data=msg, is_extended_id=True)
                bus.send(msg_send)
                time.sleep(0.4)


if __name__ == '__main__':
    try:
        channel = Channel(name="can1", bitrate=BITRATE_500)
        main()
    except KeyboardInterrupt:
        print("\r\nInterruption de l'utilisateur")
    finally:
        channel.stop()
