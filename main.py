from ast import While
import os
from threading import TIMEOUT_MAX
from typing import final
import can

from constances import CAN_CFG

sem = CAN_CFG.get("SEM")
ID_DIAG = sem.get("ID_DIAG")
ID_REPLY = sem.get("ID_REPLY")
BITRATE_125 = "125000"
BITRATE_250 = "250000"
BITRATE_500 = "500000"


def data_print(msg):
    try:
        print(f"ID: 0x{msg.arbitration_id:02X} - data: {' '.join([f'{a:02X}' for a in msg.data])}")
    except AttributeError:
        pass


def main(timeout = 50):
    id, data, multiline  = 0x00, bytearray(), False
    data_zero = 0x21

    bus = can.Bus(channel='can0', interface='socketcan')# socketcan
    msg = can.Message(arbitration_id=ID_DIAG, data=[0x03, 0x22, 0xF1, 0x81], is_extended_id=True)
    bus.send(msg)

    while timeout != 0:
        msg_recv = bus.recv(0.1)
        if msg_recv and msg_recv.arbitration_id == ID_REPLY:
            if msg_recv.data[0] == 0x10:
                data.extend(msg_recv.data[1:])
                msg = can.Message(arbitration_id=ID_DIAG, data=sem.get("DataExtended"), is_extended_id=True)
                bus.send(msg)
                multiline = True
            elif msg_recv.data[0] == data_zero:
                data.extend(msg_recv.data[1:])
                data_zero += 1
            elif not multiline and msg_recv.dlc != 0:
                data =  msg_recv.data
            data_print(msg_recv)
        timeout -= 1

    print(f"data: {' '.join([f'{a:02X}' for a in data])}")
    print(f"Software: {' '.join([f'{(a - 0x30):01X}' for a in data[6:] if a != 0])}")



if __name__ == '__main__':
    try:
        os.system(f'sudo ip link set can0 type can bitrate {BITRATE_500}')
        os.system('sudo ifconfig can0 up')
        main()
    except KeyboardInterrupt:
        print("Interruption de l'utilisateur")
    finally:
        os.system('sudo ifconfig can0 down')
