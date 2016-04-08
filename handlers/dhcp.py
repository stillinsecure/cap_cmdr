import utility
from dpkt import dhcp, ip, ethernet
from core import BaseHandler, ProtocolDef

class DHCPHandler(BaseHandler):

    def __init__(self):
        protocol_def = ProtocolDef(ethernet.ETH_TYPE_IP, ip.IP_PROTO_UDP, 67)
        super(DHCPHandler, self).__init__(protocol_def, 'DHCP')

    def process(self, eth_hdr, ip_hdr):
        udp_hdr = ip_hdr.data
        dhcp_pkt = dhcp.DHCP(udp_hdr.data)

        if dhcp_pkt.op == dhcp.DHCP_OP_REQUEST:
            return self.protocol_def.key, 'N/A', dhcp.DHCP_OP_REQUEST

    def format_query(self, query, sub_type):
        return query

    def format_sub_type(self, sub_type):
        return 'DHCP'