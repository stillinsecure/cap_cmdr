from netaddr import EUI, IPAddress
from datetime import datetime

def int_to_ip(ip_number):
    if ip_number is None:
        return None
    return str(IPAddress(ip_number))

def int_to_mac(mac_number):
    if mac_number is None:
        return None
    eui = EUI(mac_number)
    return  str(eui)

def timestamp_to_str(timestamp):
    if timestamp is None:
        return None
    return datetime.fromtimestamp(timestamp).strftime('%c')