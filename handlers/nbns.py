from dpkt import ip, dns, netbios, ethernet
from core import BaseHandler, ProtocolDef

class NBNSHandler(BaseHandler):

    def __init__(self):
        protocol_def = ProtocolDef(ethernet.ETH_TYPE_IP, ip.IP_PROTO_UDP, 137)
        super(NBNSHandler, self).__init__(protocol_def, 'NBNS')

    def process(self, eth_hdr, ip_hdr):
        udp_hdr = ip_hdr.data
        dns_pkt = dns.DNS(udp_hdr.data)

        for ques in dns_pkt.qd:
            query = netbios.decode_name(ques.name)
            return self.protocol_def.key, query, 0