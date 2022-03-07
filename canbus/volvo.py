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
    HW_MANU = SEM.get('VehicleManufacturerECUHardwareNumberDataIdentifier')

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.debug = kwargs.get("debug", False)

    def get_software(self, timeout: int):
        self.send_messages(self.ID_DIAG, self.APP_SOFT)
        data = self._get_data(timeout, self.APP_SOFT)

        if self.debug:
            print(f"data: {' '.join([f'{a:02X}' for a in data])}")
        print(f"Software: {data[6:].decode()}")

    def get_vin(self, timeout: int):
        self.send_messages(self.ID_DIAG, self.VIN)
        data = self._get_data(timeout, self.VIN)

        if self.debug:
            print(f"data: {' '.join([f'{a:02X}' for a in data])}")
        print(f"vin: {data[4:].decode()}")
    
    def get_ecu_hw_brand(self, timeout: int):
        self.send_messages(self.ID_DIAG, self.HW_MANU)
        data = self._get_data(timeout, self.HW_MANU)

        if self.debug:
            print(f"data: {' '.join([f'{a:02X}' for a in data])}")
        print(f"ECU HW Brand: {data[4:].decode()}")
    
    def _get_data(self, timeout, msg_send):
        data_zero, data, multiline  = 0x21, bytearray(), -1
        while timeout != 0 and multiline != 0:
            msg_recv = self.recv(0.1)
            if msg_recv and msg_recv.arbitration_id == self.ID_REPLY:
                if msg_recv.data[0] == 0x10 and msg_recv.data[3] == msg_send[2] and msg_recv.data[4] == msg_send[3]:
                    multiline = ceil((int(msg_recv.data[1]) + 1) / 7) - 1
                    print(multiline)
                    data.extend(msg_recv.data[1:])
                    self.send_messages(self.ID_DIAG, self.DATA_EXT)
                elif msg_recv.data[0] == data_zero:
                    data.extend(msg_recv.data[1:])
                    data_zero += 1
                    multiline -= 1
                elif multiline == -1 and msg_recv.dlc != 0:
                    data =  msg_recv.data
                self.data_print(msg_recv)
            timeout -= 1
        return data
