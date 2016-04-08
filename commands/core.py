import re
import utility
from request import Request

class BaseCommand(object):

    def __init__(self, handlers, arg, layout, fields, cmd_help, choices):
        self.handlers = handlers
        self.arg = arg
        self.layout = layout
        self.fields = fields
        self.cmd_help = cmd_help
        self.choices = choices

    def sanitize_field_name(self, value):
        return re.sub(' ', '', value)

    def get_field_names(self):
        if self.fields is None:
            return None
        field_names = [item[0] for item in self.fields]
        return self.layout.format(*field_names)

    def get_cmd_regex(self):
        cmd_reg_ex = '^({0})'.format(self.arg)
        if self.choices is not None:
            cmd_reg_ex += '\s*(?i)('
            for choice in self.choices:
                cmd_reg_ex += '{0}|'.format(choice)
            cmd_reg_ex += ')'
        cmd_reg_ex += '$'
        return cmd_reg_ex

class ActionCommand(BaseCommand):

    def execute(self, handlers, args):
        result = self.query(handlers, args)
        return result

class QueryCommand(BaseCommand):

    def execute(self, handlers, args):
        select_qry = self.query(handlers, args).dicts()

        for values in select_qry:
            row = []
            if Request.sub_type.name in values:
                sub_type = values[Request.sub_type.name]
            else:
                sub_type = None
            for alias, field in self.fields:
                key = self.sanitize_field_name(alias)
                value = values[key]
                if field.db_column == Request.type.name:
                    handler = handlers[value]
                    value = handler.display_col
                elif field.db_column == Request.ip.name:
                    value = utility.int_to_ip(value)
                elif field.db_column == Request.mac.name:
                    value = utility.int_to_mac(value)
                elif field.db_column == Request.query.name:
                    if sub_type is not None:
                        value = handler.format_query(value, sub_type)
                elif field.db_column == Request.sub_type.name:
                    value = handler.format_sub_type(value)
                row.append(value)
            yield self.layout.format(*row)

    def select(self):
        temp = []
        for alias, field in self.fields:
            key = self.sanitize_field_name(alias)
            field = field.alias(key)
            temp.append(field)
        temp.append(Request.type)
        return Request.select(*temp)

