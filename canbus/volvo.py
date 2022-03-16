from math import ceil

from . import CanBus
from constances import CAN_CFG


class Sem(CanBus):
    """
    Class for diagnosis of SEM products
    """
    SEM = CAN_CFG.get("SEM")
    ID_DIAG = SEM.get("ID_DIAG")
    ID_REPLY = SEM.get("ID_REPLY")
    DATA_EXT = SEM.get("DataExtended")
    APP_SOFT = SEM.get("ApplicationSoftwareIdentificationDataIdentifier")
    APP_DATA = SEM.get("ApplicationDataIdentificationDataIdentifier")
    COM_DIAG = SEM.get("CommonDiagnosticsDataRecord61828")
    VIN = SEM.get("VehicleIdentificationNumber")
    HW_MANU = SEM.get("VehicleManufacturerECUHardwareNumberDataIdentifier")

    def __init__(self, *args, **kwargs):
        """ Initialize class """
        super().__init__(self, *args, **kwargs)
        self.debug = kwargs.get("debug", False)

    def get_software(self, timeout: int):
        """
        Read ApplicationSoftwareIdentificationDataIdentifier
        :param timeout: Timeout for the data read
        :return: Software value
        """
        self.send_messages(self.ID_DIAG, self.APP_SOFT)
        data = self._get_data(timeout, self.APP_SOFT)
        return self._decode(data[6:])
    
    def get_data_identify(self, timeout: int):
        """
        Read ApplicationDataIdentificationDataIdentifier
        :param timeout: Timeout for the data read
        :return: ASM value and HW value
        """
        self.send_messages(self.ID_DIAG, self.APP_DATA)
        data = self._get_data(timeout, self.APP_DATA)
        asm, hw = self._decode(data[6:17]), self._decode(data[17:])
        return asm, hw

    def get_vin(self, timeout: int):
        """
        Read VehicleIdentificationNumber
        :param timeout: Timeout for the data read
        :return: VIN value
        """
        self.send_messages(self.ID_DIAG, self.VIN)
        data = self._get_data(timeout, self.VIN)
        return self._decode(data[4:])
    
    def get_ecu_hw_brand(self, timeout: int):
        """
        Read VehicleManufacturerECUHardwareNumberDataIdentifier
        :param timeout: Timeout for the data read
        :return: ECU HW value
        """
        self.send_messages(self.ID_DIAG, self.HW_MANU)
        data = self._get_data(timeout, self.HW_MANU)
        return self._decode(data[4:])

    def get_com_diag(self, timeout: int):
        """
        Read CommonDiagnosticsDataRecord61828
        :param timeout: Timeout for the data read
        :return: data value
        """
        self.send_messages(self.ID_DIAG, self.COM_DIAG)
        data = self._get_data(timeout, self.COM_DIAG)
        return self._decode(data[6:])
    
    def _get_data(self, timeout, msg_send):
        """
        Internal method of handling multiple CAN frames
        :param timeout: Timeout for the data read
        :param msg_send: CAN frame of the request to check the response
        :return: List of data retrieved in the different CAN frames
        """
        data_zero, data, multiline  = 0x21, bytearray(), -1
        while timeout > 0 and multiline != 0:
            msg_recv = self.recv(0.1)
            if msg_recv and msg_recv.arbitration_id == self.ID_REPLY:
                if msg_recv.data[0] == 0x10 and msg_recv.data[3] == msg_send[2] and msg_recv.data[4] == msg_send[3]:
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
        if self.debug:
            print(f"data: {' '.join([f'{a:02X}' for a in data])}")
        return data
