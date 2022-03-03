import time
from binascii import hexlify

from canbus import CanBus
from canbus.config import Channel
from constances import CAN_CFG

BITRATE_125 = 125000
BITRATE_250 = 250000
BITRATE_500 = 500000

sem = CAN_CFG.get("SEM")
ID_DIAG = sem.get("ID_DIAG")
ID_REPLY = sem.get("ID_REPLY")
app_soft = sem.get('ApplicationSoftwareIdentificationDataIdentifier')
app_data = sem.get('ApplicationDataIdentificationDataIdentifier')
com_diag = sem.get('CommonDiagnosticsDataRecord61828')
vin = sem.get('VehicleIdentificationNumber')


def main():
    can1 = CanBus(channel='can1')

    while True:
        msg = can1.recv()
        can1.data_print(msg)

        if msg.arbitration_id == ID_DIAG:
            if msg.data == bytearray(app_soft):
                print("OK => ApplicationSoftwareIdentificationDataIdentifer")
                msg_list = [
                    [0x10, 0x10, 0x62, 0xF1, 0x81, 0x01, 0x05, 0x32],
                    [0x21, 0x32, 0x36, 0x36, 0x39, 0x34, 0x37, 0x36],
                    [0x22, 0x43, 0x30, 0x31, 0x00, 0x00, 0x00, 0x00]
                ]
                can1.send_messages(ID_REPLY, msg_list, True)

            elif msg.data == bytearray(app_data):
                print("OK => ApplicationDataIdentificationDataIdentifier")
                msg_list = [
                    [0x10, 0x1C, 0x62, 0xF1, 0x82, 0x02, 0x07, 0x32],
                    [0x21, 0x33, 0x34, 0x33, 0x37, 0x33, 0x38, 0x36],
                    [0x22, 0x50, 0x30, 0x31, 0x07, 0x32, 0x33, 0x34],
                    [0x23, 0x33, 0x37, 0x33, 0x39, 0x31, 0x50, 0x30],
                    [0x24, 0x31, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00] 
                ]
                can1.send_messages(ID_REPLY, msg_list, True)
            
            elif msg.data == bytearray(vin):
                print("OK =>VehicleIdentificationNumber")
                msg_list = [
                    [0x10, 0x14, 0x62, 0xF1, 0x90, 0x56, 0x46, 0x33],
                    [0x21, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20],
                    [0x22, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20],
                ]
                can1.send_messages(ID_REPLY, msg_list, True)


if __name__ == '__main__':
    try:
        channel = Channel(name="can1", bitrate=BITRATE_500)
        main()
    except KeyboardInterrupt:
        print("\r\nInterruption de l'utilisateur")
    finally:
        channel.stop()
