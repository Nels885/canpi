from canbus.config import Channel
from canbus.volvo import Sem
from constances import CAN_CFG

BITRATE_125 = 125000
BITRATE_250 = 250000
BITRATE_500 = 500000

def main(channel, timeout = 50):
    sem = Sem(channel=channel.name)
    # sem = Sem(channel="can0")

    print("## Lecture des informations Software SEM ##")
    soft = sem.get_software(timeout)
    print(f"Software: {soft}")

    print("\r\n## Lecture du V.I.N. SEM ##")
    vin = sem.get_vin(timeout)
    print(f"vin: {vin}")

    print("\r\n## Lecture du hardware ECU fabriquant SEM ##")
    hw = sem.get_ecu_hw_brand(timeout)
    print(f"ECU HW Brand: {hw}")

if __name__ == '__main__':
    try:
        channel = Channel(name='can0', bitrate=BITRATE_500)
        main(channel=channel)
    except KeyboardInterrupt:
        print("Interruption de l'utilisateur")
    # finally:
    #     channel.stop()
