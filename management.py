import datetime
import imp
import inspect
import os
import re

import dpkt.arp
import dpkt.ethernet
import dpkt.icmp
import dpkt.ip
import dpkt.tcp
import dpkt.udp

from commands.core import ActionCommand, QueryCommand
from handlers.core import BaseHandler, ProtocolDef
from request import Request


class HandlerManager(object):

    def __init__(self):
        self.handlers = dict()
        self.commands = dict()

        temp = self.load_classes([BaseHandler,], 'handlers')
        for handler_cls in temp:
            handler = handler_cls()
            self.handlers[handler.protocol_def.key] = handler
        temp = self.load_classes([QueryCommand, ActionCommand], 'commands')
        for cmd_cls in temp:
            cmd = cmd_cls(self.handlers)
            self.commands[cmd.arg] = cmd

    def load_classes(self, base_classes, package_name):
        classes = []
        for base_class in base_classes:
            for path in os.listdir(package_name):
                base, ext = os.path.splitext(path)
                if base != '__init__' and ext == '.py':
                    module = imp.load_source(package_name + '.' + base, package_name + '/' + path)
                    for cls_name, cls_type in inspect.getmembers(module):
                        if cls_name == base_class.__name__:
                            continue
                        if inspect.isclass(cls_type) \
                            and base_class.__name__ in [item.__name__ for item in inspect.getmro(cls_type)] \
                            and cls_type not in classes:
                            classes.append(cls_type)
        return classes

    def exec_command(self, user_input):
        for cmd in self.commands.values():
            match = re.match(cmd.get_cmd_regex(), user_input)
            if match is not None:
                return cmd.get_field_names(), cmd.execute(self.handlers, match.groups())

    def _get_handler(self, data):
        eth_hdr = dpkt.ethernet.Ethernet(data)
        ip_hdr = None
        protocol_def = None

        # ARP
        if eth_hdr.type == dpkt.ethernet.ETH_TYPE_ARP:
            protocol_def = ProtocolDef(dpkt.ethernet.ETH_TYPE_ARP, 0, 0)
        # IP
        elif eth_hdr.type == dpkt.ethernet.ETH_TYPE_IP:
            ip_hdr = eth_hdr.data
            # ICMP
            if ip_hdr.p == dpkt.ip.IP_PROTO_ICMP:
                protocol_def = ProtocolDef(dpkt.ethernet.ETH_TYPE_IP, dpkt.ip.IP_PROTO_ICMP, 0)
            # TCP
            elif ip_hdr.p == dpkt.ip.IP_PROTO_TCP:
                tcp_hdr = ip_hdr.data
                protocol_def = ProtocolDef(dpkt.ethernet.ETH_TYPE_IP, dpkt.ip.IP_PROTO_TCP, tcp_hdr.dport)
            # UDP
            elif ip_hdr.p == dpkt.ip.IP_PROTO_UDP:
                udp_hdr = ip_hdr.data
                protocol_def = ProtocolDef(dpkt.ethernet.ETH_TYPE_IP, dpkt.ip.IP_PROTO_UDP, udp_hdr.dport)

        if protocol_def is not None and protocol_def.key in self.handlers:
            return self.handlers[protocol_def.key], eth_hdr, ip_hdr

        return None, None, None

    def process_data(self, data, captured):
        handler, eth_hdr, ip_hdr = self._get_handler(data)
        ip = None
        if handler is not None:
            if ip_hdr is not None:
                ip = int(ip_hdr.src.encode('hex'), 16)
            mac = int(eth_hdr.src.encode('hex'), 16)
            try:
                key, query, sub_type = handler.process(eth_hdr, ip_hdr)
                captured = datetime.datetime.fromtimestamp(captured)
                Request.create(type=key, query=query, ip=ip, mac=mac, captured=captured, sub_type=sub_type)
            except:
                print 'here'
