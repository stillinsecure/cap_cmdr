import pcap
from management import HandlerManager

class Capture(object):

    def __init__(self, pcap_dev, timeout, callback):
        self.__pcap_dev = pcap_dev

    def start(self, pcap_dev, timeout):
        mgr = HandlerManager()
        cap = pcap.pcap(name=pcap_dev, timeout_ms=timeout)
        while True:
            pkt = cap.next()
            # Handle timeouts packet will be None
            if pkt is None:
                continue
            timestamp, data = pkt

            mgr.process_data(data, timestamp)
