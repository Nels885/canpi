from math import ceil

from . import CanBus
from constances import CAN_CFG


class Cvm(CanBus):
    CVM = CAN_CFG.get('CVM')
    ID_DIAG = CVM.get("ID_DIAG")
    ID_REPLY = CVM.get("ID_REPLY")
    DATA_EXT = CVM.get("DataExtended")
    OPEN_SESSION = CVM.get("SessionOpen")
    DTC_NB = CVM.get("ReportNumberOfDTCByStatusMask")
    DTC_LIST = CVM.get("ReportDTCbyStatusMask")
    DTC_CLEAR = CVM.get("ClearDTC")
    IDENT_SYS = CVM.get("ReadDataByIdentificationSystem")
    ZONE_SYS = CVM.get("ReadDataByZoneIdentification")


    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.debug = kwargs.get("debug", False)

    def get_dtc_list(self, timeout: int):
        self.send_messages(self.ID_DIAG, self.DTC_LIST)
        data = self._get_data(timeout)

        if self.debug:
            print(f"data: {' '.join([f'{a:02X}' for a in data])}")
        defaults, default = [], []
        for nb, byte in enumerate(data[4:]):
            if (nb + 1) % 4 != 0:
                print(f"{byte:02X}", end="")
                if (nb + 1) % 2 == 0:
                    print(" ", end="")
            else:
                print(f"{byte:02X}")
        return data

    def get_dtc_number(self, timeout: int):
        self.send_messages(self.ID_DIAG, self.DTC_NB)
        data = self._get_data(timeout)

        if self.debug:
            print(f"data: {' '.join([f'{a:02X}' for a in data])}")
        print(f"DTC number: {data[-1]:02X}")
        return data
    
    def set_clear_dtc(self, timeout: int):
        self.send_messages(self.ID_DIAG, self.OPEN_SESSION)
        self._get_data(timeout)
        self.send_messages(self.ID_DIAG, self.DTC_CLEAR)
        data = self._get_data(timeout)

        if self.debug:
            print(f"data: {' '.join([f'{a:02X}' for a in data])}")
        return data

    def get_identify_system(self, timeout: int):
        self.send_messages(self.ID_DIAG, self.IDENT_SYS)
        data = self._get_data(timeout)

        if self.debug:
            print(f"data: {' '.join([f'{a:02X}' for a in data])}")
        return data
    
    def get_zone_identify(self, timeout: int):
        self.send_messages(self.ID_DIAG, self.ZONE_SYS)
        data = self._get_data(timeout)

        if self.debug:
            print(f"data: {' '.join([f'{a:02X}' for a in data])}")
        return data
     
    def _get_data(self, timeout):
        data_zero, data, multiline  = 0x21, bytearray(), -1
        while timeout > 0 and multiline != 0:
            msg_recv = self.recv(0.1)
            if msg_recv and msg_recv.arbitration_id == self.ID_REPLY:
                if msg_recv.data[0] == 0x10: 
                    multiline = ceil((int(msg_recv.data[1]) + 1) / (msg_recv.dlc - 1)) - 1
                    data.extend(msg_recv.data[1:])
                    self.send_messages(self.ID_DIAG, self.DATA_EXT)
                elif msg_recv.data[0] == data_zero:
                    data.extend(msg_recv.data[1:])
                    data_zero += 1
                    multiline -= 1
                elif multiline == -1 and msg_recv.dlc != 0:
                    data =  msg_recv.data
                    timeout = 0
                if self.debug:
                    self.data_print(msg_recv)
            timeout -= 1
        return data
