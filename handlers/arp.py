import utility
from dpkt import arp, ethernet
from core import BaseHandler, ProtocolDef

class ARPHandler(BaseHandler):

    def __init__(self):
        protocol_def = ProtocolDef(ethernet.ETH_TYPE_ARP, 0, 0)
        super(ARPHandler, self).__init__(protocol_def, 'ARP')

    def process(self, eth_hdr, ip_hdr):
        arp_pkt = eth_hdr.data
        if arp_pkt.op == arp.ARP_OP_REQUEST:
            query = int(arp_pkt.tpa.encode('hex'), 16)
            return self.protocol_def.key, query, arp.ARP_OP_REQUEST

    def format_query(self, query, sub_type):
        if sub_type == arp.ARP_OP_REQUEST:
            return utility.int_to_ip(query)
        return query

    def format_sub_type(self, sub_type):
        if sub_type == arp.ARP_OP_REQUEST:
            return 'ARP Request'
