import re
import requests

from canbus.config import Channel
from canbus.volvo import Sem
from usb_scanner import Reader
from constances import CAN_CFG, URL, TOKEN

BITRATE_125 = 125000
BITRATE_250 = 250000
BITRATE_500 = 500000


def barcode_check(scan, regex):
    while True:
        barcode = scan.read()
        if re.match(regex, str(barcode)):
            print(f"\rbarcode: {barcode}   ")
            break
        print("\rMauvais code barre !!!", end="")
    return barcode

def barcode_scan(scan):
    print("\r\n## Attente lecture ID_NUMBER ##")
    id_number = barcode_check(scan, r"^V\d{9}$")
    
    print("\r\n## Attente lecteur PF_CODE ##")
    pf_code = barcode_check(scan, r"^PF\w{16}$")

    return id_number, pf_code


def api_rest(id_number, pf_code, vin):
    print("\r\n## CSD Dashboard API ##")
    if id_number and pf_code and len(vin) == 17:
        msg = f"API url:{URL} -"
        payload = {'identify_number': id_number, 'barcode': pf_code, 'vin': vin}
        try:
            response = requests.post(url=URL, params={'auth_token': TOKEN}, data=payload)
            if response.status_code == 200:
                print(response.json())
                return True
            elif response.status_code == 401:
                print(msg, "connection refused")
            elif response.status_code == 408:
                print(msg, "connection timeout")
            else:
                print(msg, "connection error")
        except requests.exceptions.ConnectionError as err:
            print(msg, "host not found")
    else:
        print("VIN non présent !!!")
    return False


def main(channel, timeout = 50):
    sem = Sem(channel=channel.name)
    scan = Reader()
    # sem = Sem(channel="can0")

    while True:
        print("\r\n===================================")
        print("|       SEM REMAN read VIN        |")
        print("===================================")
        
        id_number, pf_code = barcode_scan(scan)

        print("## Lecture des informations Software SEM ##")
        soft = sem.get_software(timeout)
        print(f"Software: {soft}")

        print("\r\n## Lecture du V.I.N. SEM ##")
        vin = sem.get_vin(timeout)
        print(f"vin: {vin}")

        print("\r\n## Lecture du hardware ECU fabriquant SEM ##")
        hw = sem.get_ecu_hw_brand(timeout)
        print(f"ECU HW Brand: {hw}")

        api_rest(id_number, pf_code, vin)
        


if __name__ == '__main__':
    try:
        channel = Channel(name='can0', bitrate=BITRATE_500)
        main(channel=channel)
    except KeyboardInterrupt:
        print("Interruption de l'utilisateur")
    finally:
        channel.stop()
