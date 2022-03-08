import time
from binascii import hexlify

from canbus import CanBus
from canbus.config import Channel
from constances import CAN_CFG

BITRATE_125 = 125000
BITRATE_250 = 250000
BITRATE_500 = 500000

cvm = CAN_CFG.get("CVM")
ID_DIAG = cvm.get("ID_DIAG")
ID_REPLY = cvm.get("ID_REPLY")
dtc_list = cvm.get("ReportDTCbyStatusMask")
dtc_nb = cvm.get("ReportNumberOfDTCByStatusMask")


def main(channel):
    can1 = CanBus(channel=channel.name)

    while True:
        msg = can1.recv()
        can1.data_print(msg)

        if msg.arbitration_id == ID_DIAG:
            if msg.data == bytearray(dtc_list):
                print("OK => ReportDTCbyStatusMask")
                msg_list = [
                    [0x10, 0x13, 0x59, 0x02, 0x89, 0x91, 0x7F, 0x00],
                    [0x21, 0x89, 0x90, 0x04, 0x96, 0x89, 0xDF, 0x00],
                    [0x22, 0x00, 0x89, 0xD2, 0x13, 0x81, 0x89]
                ]
                can1.send_messages(ID_REPLY, msg_list)
        
            elif msg.data == bytearray(dtc_nb):
                print("OK => ReportNumberOfDTCByStatusMask")
                msg_list = [0x06, 0x59, 0x01, 0x09, 0x00, 0x00, 0x04]
                can1.send_messages(ID_REPLY, msg_list)


if __name__ == '__main__':
    try:
        channel = Channel(name="can1", bitrate=BITRATE_500)
        main(channel)
    except KeyboardInterrupt:
        print("\r\nInterruption de l'utilisateur")
    finally:
        channel.stop()
