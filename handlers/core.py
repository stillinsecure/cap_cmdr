class ProtocolDef(object):

    def __init__(self, ether_type, transport_type, port):
        self.ether_type = ether_type
        self.transport_type = transport_type
        self.port = port
        self.key = int(str(self.ether_type) + str(self.transport_type) + str(self.port))


class BaseHandler(object):

    # http://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml
    # http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
    def __init__(self, protocol_def, display_col):
        self.protocol_def = protocol_def
        self.display_col = display_col