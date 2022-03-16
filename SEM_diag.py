from canbus.config import Channel
from canbus.volvo import Sem
from constances import CAN_CFG

BITRATE_125 = 125000
BITRATE_250 = 250000
BITRATE_500 = 500000

def main(channel, timeout = 50):
    sem = Sem(channel=channel.name, debug=False)
    # sem = Sem(channel="can0")

    print("## Lecture des informations Software SEM ##")
    soft = sem.get_software(timeout)
    print(f"Software: {soft}")

    print("\r\n## Lecture des données d'identification SEM ##")
    asm, hw = sem.get_data_identify(timeout)
    print(f"ASM: {asm} - HW: {hw}")

    print("\r\n## Lecture du V.I.N. SEM ##")
    vin = sem.get_vin(timeout)
    print(f"vin: {vin}")

    print("\r\n## Lecture du hardware ECU fabriquant SEM ##")
    ecu_hw = sem.get_ecu_hw_brand(timeout)
    print(f"ECU HW Brand: {ecu_hw}")

    print("\r\n## Lecture Common Diag SEM ##")
    com_diag = sem.get_com_diag(timeout)
    print(f"Common diag: {com_diag}")


if __name__ == '__main__':
    try:
        channel = Channel(name='can0', bitrate=BITRATE_500)
        main(channel=channel)
    except KeyboardInterrupt:
        print("Interruption de l'utilisateur")
    # finally:
    #     channel.stop()
