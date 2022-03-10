import argparse

from canbus.config import Channel
from canbus.psa import Cvm
from constances import CAN_CFG

BITRATE_125 = 125000
BITRATE_250 = 250000
BITRATE_500 = 500000


def add_arguments():
    parser = argparse.ArgumentParser(description="PSA CVM diagnostic tools")
    parser.add_argument("--clear_dtc", action="store_true", help="Clear defaults of CVM module")
    parser.add_argument("--channel", type=str, default="can0", help="can0 or can1, default=can0")
    parser.add_argument("--bitrate", type=int, default=BITRATE_125, help="Bitrate of CAN Bus, default=125000")
    return parser.parse_args()


def main(args, channel, timeout = 50):
    cvm = Cvm(channel=channel.name, debug=False)
    if args.clear_dtc:
        print("## Effacement des défauts ##")
        data = cvm.set_clear_dtc(timeout)
        print(f"data: {' '.join([f'{a:02X}' for a in data])}")
    else:
        print("## Lecture identification Système ##")
        data = cvm.get_identify_system(timeout)
        print(f"Référence Matériel: {''.join([f'{a:02X}' for a in data[4:9]])}")
        print(f"Référence complémentaire Matériel: {''.join([f'{a:02X}' for a in data[11:16]])}")

        print("\r\n## Lecture zone identification ##")
        data = cvm.get_zone_identify(timeout)
        print(f"Identification de la calibration: {'.'.join([f'{a:02X}' for a in data[15:17]])}")
        print(f"Numéro du fichier de la calibration: 96{''.join([f'{a:02X}' for a in data[25:]])}80")
        print(f"Nombre de téléchargement: {data[24]:02X}")

        print("\r\n## Lecture nombre de defauts CVM ##")
        data = cvm.get_dtc_number(timeout)

        print("\r\n## Lecture des defauts CVM ##")
        cvm.get_dtc_list(timeout)


if __name__ == '__main__':
    args = add_arguments()
    try:
        channel = Channel(name=args.channel, bitrate=args.bitrate)
        main(args, channel=channel)
    except KeyboardInterrupt:
        print("Interruption de l'utilisateur")
    finally:
        channel.stop()
