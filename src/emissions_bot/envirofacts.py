from __future__ import annotations

import dataclasses
from typing import List, Literal, Optional


ENVIROFACTS_URL = 'https://data.epa.gov/efservice'


class Query:
    tables: List[_Table]

    def __init__(self):
        self.tables = list()
    
    def table(self, table_name: str):
        self.tables.append(_Table(table_name))
        return self
    
    def column_equals(self, column_name: str, column_value: str):
        self.tables[-1].column_name = column_name
        self.tables[-1].column_value = column_value
        self.tables[-1].operator = '='
        return self
    
    def column_nequals(self, column_name: str, column_value: str):
        self.tables[-1].column_name = column_name
        self.tables[-1].column_value = column_value
        self.tables[-1].operator = '!='
        return self
    
    def column_less(self, column_name: str, column_value: str):
        self.tables[-1].column_name = column_name
        self.tables[-1].column_value = column_value
        self.tables[-1].operator = '<'
        return self
    
    def column_greater(self, column_name: str, column_value: str):
        self.tables[-1].column_name = column_name
        self.tables[-1].column_value = column_value
        self.tables[-1].operator = '>'
        return self
    
    def column_begins(self, column_name: str, column_value: str):
        self.tables[-1].column_name = column_name
        self.tables[-1].column_value = column_value
        self.tables[-1].operator = 'BEGINNING'
        return self
    
    def column_contains(self, column_name: str, column_value: str):
        self.tables[-1].column_name = column_name
        self.tables[-1].column_value = column_value
        self.tables[-1].operator = 'CONTAINING'
        return self
    

@dataclasses.dataclass
class _Table:
    table_name: str
    column_name: str | None = None
    operator: Literal['=', '!=', '<', '>', 'BEGINNING', 'CONTAINING'] | None = None
    column_value: str | None = None

