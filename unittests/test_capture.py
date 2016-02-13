from unittest import TestCase
from capture import Capture

class TestCapture(TestCase):

    def test_arp_capture(self):
        cap = Capture('arp', 10000, None)
        cap.start('/Users/darren/PycharmProjects/bc_enum/unittests/arp.pcap', 10000)

    def test_nbns_capture(self):
        cap = Capture('nbns', 10000, None)
        cap.start('nbns.pcap', 10000)
