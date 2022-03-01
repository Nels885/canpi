import os
import time
import can
from binascii import hexlify

from constances import CAN_CFG

sem_cfg = CAN_CFG.get("SEM")
ID_DIAG = sem_cfg.get("ID_DIAG")
ID_REPLY = sem_cfg.get("ID_REPLY")
BITRATE_125 = "125000"
BITRATE_250 = "250000"
BITRATE_500 = "500000"

msg_identifier=[0x03, 0x22, 0xF1, 0x81]


def main():
    bus = can.Bus(channel='can1', interface='socketcan')# socketcan

    while True:
        msg = bus.recv()
        print(f"ID: {hex(msg.arbitration_id)} - data: {' '.join([hex(a) for a in msg.data])}")

        if msg.arbitration_id == ID_DIAG and msg.data == bytearray(msg_identifier):
            print("OK => ApplicationSoftwareIdentificationDataIdentifer")
            msg_list = [
                [0x10, 0x10, 0x62, 0xF1, 0x81, 0x01, 0x05, 0x32],
                [0x21, 0x32, 0x36, 0x36, 0x39, 0x34, 0x37, 0x36],
                [0x22, 0x43, 0x30, 0x31, 0x00, 0x00, 0x00, 0x00]
            ]
            for msg in msg_list:
                msg_send = can.Message(arbitration_id=ID_REPLY, data=[0x10, 0x10, 0x62, 0xF1, 0x81, 0x01, 0x05, 0x32], is_extended_id=True)
                bus.send(msg_send)
                time.sleep(0.4)


if __name__ == '__main__':
    try:
        os.system(f'sudo ip link set can1 type can bitrate {BITRATE_500}')
        os.system('sudo ifconfig can1 up')
        main()
    except KeyboardInterrupt:
        print("\r\nInterruption de l'utilisateur")
    finally:
        os.system('sudo ifconfig can1 down')