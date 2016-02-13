from dpkt import ip, dns, ethernet
from core import BaseHandler, ProtocolDef

class LLMNRHandler(BaseHandler):

    def __init__(self):
        protocol_def = ProtocolDef(ethernet.ETH_TYPE_IP, ip.IP_PROTO_UDP, 5355)
        super(LLMNRHandler, self).__init__(protocol_def, 'LLMNR')

    def process(self, eth_hdr, ip_hdr):
        udp_hdr = ip_hdr.data
        dns_pkt = dns.DNS(udp_hdr.data)

        for ques in dns_pkt.qd:
            query = ques.name
            return self.protocol_def.key, query, 0