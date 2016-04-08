from request import Request
from peewee import *
from core import QueryCommand

class StatisticsCommand(QueryCommand):

    def __init__(self, handlers):
        super(self.__class__, self).__init__(
            choices=[item.display_col for item in handlers.values()],
            handlers=handlers,
            arg='s',
            cmd_help='Statistics for the capture',
            layout='{}{}{}{}',
            fields=[('Type', Request.type),
                    ('Count', fn.COUNT(Request.type)),
                    ('First Captured',fn.Min(Request.captured)),
                    ('Last Captured',fn.Max(Request.captured))]
        )

    def query(self, handlers, args):
        return self.select().group_by(Request.type)