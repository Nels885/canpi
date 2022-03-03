from canbus.config import Channel
from canbus.volvo import Sem
from constances import CAN_CFG

BITRATE_125 = 125000
BITRATE_250 = 250000
BITRATE_500 = 500000

def main(timeout = 50):
    sem = Sem(channel='can0')

    print("## Lecture des informations Software SEM ##")
    sem.get_software(timeout)

    print("\r\n## Lecture du V.I.N. SEM ##")
    sem.get_vin(timeout)

    print("\r\n## Lecture du harware ECU fabriquant SEM ##")
    sem.get_ecu_hw_brand(timeout)

if __name__ == '__main__':
    try:
        channel = Channel(name='can0', bitrate=BITRATE_500)
        main()
    except KeyboardInterrupt:
        print("Interruption de l'utilisateur")
    finally:
        channel.stop()
