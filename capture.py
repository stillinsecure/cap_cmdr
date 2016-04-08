import pcap
import thread

from management import HandlerManager

class Capture(object):

    def start(self, pcap_dev, timeout):
        thread.start_new_thread(self._start, (pcap_dev, timeout))

    def _start(self, pcap_dev, timeout):
        mgr = HandlerManager()
        cap = pcap.pcap(name=pcap_dev, timeout_ms=timeout)
        while True:
            pkt = cap.next()
            # Handle timeouts packet will be None
            if pkt is None:
                continue
            timestamp, data = pkt
            mgr.process_data(data, timestamp)
