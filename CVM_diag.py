from canbus.config import Channel
from canbus.psa import Cvm
from constances import CAN_CFG

BITRATE_125 = 125000
BITRATE_250 = 250000
BITRATE_500 = 500000

def main(channel, timeout = 50):
    # cvm = Cvm(channel=channel.name)
    cvm = Cvm(channel="can0", debug=True)

    print("## Lecture des defauts CVM ##")
    cvm.get_defaults(timeout)

if __name__ == '__main__':
    try:
        channel = Channel(name='can0', bitrate=BITRATE_500)
        main(channel="test")
    except KeyboardInterrupt:
        print("Interruption de l'utilisateur")
    # finally:
    #     channel.stop()