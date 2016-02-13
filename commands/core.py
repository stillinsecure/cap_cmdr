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
        field_names = [item[0] for item in self.fields]
        return self.layout.format(*field_names)

    def exec_query(self, handlers):

        select_qry = self.query().dicts()

        for values in select_qry:
            row = []
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
                    pass
                elif field.db_column == Request.sub_type.name:
                    value = handler.format_sub_type(value)
                row.append(value)
            yield self.layout.format(*row)

    def get_cmd_regex(self):
        cmd_reg_ex = '^({0})'.format(self.arg)
        if self.choices is not None:
            cmd_reg_ex += '\s*(?i)('
            for choice in self.choices:
                cmd_reg_ex += '{0}|'.format(choice)
            cmd_reg_ex += ')'
        cmd_reg_ex += '$'
        return cmd_reg_ex

    def select(self):
        temp = []
        for alias, field in self.fields:
            key = self.sanitize_field_name(alias)
            field = field.alias(key)
            temp.append(field)
        temp.append(Request.type)
        return Request.select(*temp)

