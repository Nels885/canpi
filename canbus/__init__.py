def data_print(msg):
    try:
        print(f"ID: 0x{msg.arbitration_id:02X} - data: {' '.join([f'{a:02X}' for a in msg.data])}")
    except AttributeError:
        pass
