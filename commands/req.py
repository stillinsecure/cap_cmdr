from request import Request
from peewee import *
from core import QueryCommand

class RequestCommand(QueryCommand):

    def __init__(self, handlers):
        super(self.__class__, self).__init__(
            choices=[item.display_col for item in handlers.values()],
            handlers=handlers,
            arg='r',
            cmd_help='List requests',
            layout='{} {} {}',
            fields=[('Type', Request.type),
                    ('sub_type', Request.sub_type),
                    ('Query', Request.query)]
        )

    def query(self, handlers, args):
        return self.select()