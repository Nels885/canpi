from math import ceil

from . import CanBus
from constances import CAN_CFG


class Cvm(CanBus):
    CVM = CAN_CFG.get('CVM')
    ID_DIAG = CVM.get("ID_DIAG")
    ID_REPLY = CVM.get("ID_REPLY")
    DATA_EXT = CVM.get("DataExtended")
    OPEN_SESSION = CVM.get("OpenSession")
    NB_DTC = CVM.get("ReportNumberOfDTCByStatusMask")
    LIST_DTC = CVM.get("ReportDTCbyStatusMask")

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.debug = kwargs.get("debug", False)

    def get_defaults(self, timeout: int):
        # self.send_messages(self.ID_DIAG, self.OPEN_SESSION, 0.1)
        self.send_messages(self.ID_DIAG, self.LIST_DTC)
        data = self._get_data(timeout)

        if self.debug:
            print(f"data: {' '.join([f'{a:02X}' for a in data])}")
        return data

  
    def _get_data(self, timeout):
        data_zero, data, multiline  = 0x21, bytearray(), -1
        while timeout != 0 and multiline != 0:
            msg_recv = self.recv(0.1)
            if msg_recv and msg_recv.arbitration_id == self.ID_REPLY:
                if msg_recv.data[0] == 0x10:
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
