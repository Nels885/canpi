from math import ceil

from . import CanBus
from constances import CAN_CFG


class Sem(CanBus):
    SEM = CAN_CFG.get("SEM")
    ID_DIAG = SEM.get("ID_DIAG")
    ID_REPLY = SEM.get("ID_REPLY")
    DATA_EXT = SEM.get("DataExtended")
    APP_SOFT = SEM.get('ApplicationSoftwareIdentificationDataIdentifier')
    COM_DIAG = SEM.get('CommonDiagnosticsDataRecord61828')
    VIN = SEM.get('VehicleIdentificationNumber')

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def set_software(self, timeout: int):
        self.send_messages(self.ID_DIAG, self.APP_SOFT, True)
        data = self._set_data(timeout, self.APP_SOFT)

        print(f"data: {' '.join([f'{a:02X}' for a in data])}")
        print(f"Software: {data[6:].decode()}")

    def set_vin(self, timeout):
        self.send_messages(self.ID_DIAG, self.VIN, True)
        data = self._set_data(timeout, self.VIN)

        print(f"data: {' '.join([f'{a:02X}' for a in data])}")
        print(f"vin: {data[4:].decode()}")
    
    def _set_data(self, timeout, msg_send):
        data_zero, data, multiline  = 0x21, bytearray(), -1
        while timeout != 0 and multiline != 0:
            msg_recv = self.recv(0.1)
            if msg_recv and msg_recv.arbitration_id == self.ID_REPLY:
                if msg_recv.data[0] == 0x10 and msg_recv.data[3] == msg_send[2] and msg_recv.data[4] == msg_send[3]:
                    multiline = ceil((int(msg_recv.data[1]) + 2) / 8)
                    print(multiline)
                    data.extend(msg_recv.data[1:])
                    self.send_messages(self.ID_DIAG, self.DATA_EXT, True)
                elif msg_recv.data[0] == data_zero:
                    data.extend(msg_recv.data[1:])
                    data_zero += 1
                elif multiline == -1 and msg_recv.dlc != 0:
                    data =  msg_recv.data
                self.data_print(msg_recv)
                multiline -= 1
            timeout -= 1
        return data
