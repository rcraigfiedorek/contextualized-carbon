from __future__ import annotations

import dataclasses
import io
from typing import List, Literal, Optional

import requests
import pandas as pd


ENVIROFACTS_URL = 'https://data.epa.gov/efservice'


class Query:

    tables: List[TableQueryData]

    def __init__(self, table_name: str | None = None):
        self.tables = list()
        if table_name:
            self.tables.append(TableQueryData(table_name))

    @property
    def url(self):
        return ENVIROFACTS_URL + ''.join(table.url_path for table in self.tables) + '/CSV'

    def table(self, table_name: str):
        self.tables.append(TableQueryData(table_name))
        return self

    def column_equals(self, column_name: str, column_value: str):
        self.tables[-1].filters.append(ColumnFilterData(
            column_name=column_name,
            operator='=',
            column_value=column_value
        ))
        return self

    def column_nequals(self, column_name: str, column_value: str):
        self.tables[-1].filters.append(ColumnFilterData(
            column_name=column_name,
            operator='!=',
            column_value=column_value
        ))
        return self

    def column_less(self, column_name: str, column_value: str):
        self.tables[-1].filters.append(ColumnFilterData(
            column_name=column_name,
            operator='<',
            column_value=column_value
        ))
        return self

    def column_greater(self, column_name: str, column_value: str):
        self.tables[-1].filters.append(ColumnFilterData(
            column_name=column_name,
            operator='>',
            column_value=column_value
        ))
        return self

    def column_begins(self, column_name: str, column_value: str):
        self.tables[-1].filters.append(ColumnFilterData(
            column_name=column_name,
            operator='BEGINNING',
            column_value=column_value
        ))
        return self

    def column_contains(self, column_name: str, column_value: str):
        self.tables[-1].filters.append(ColumnFilterData(
            column_name=column_name,
            operator='CONTAINING',
            column_value=column_value
        ))
        return self

    def get(self) -> pd.DataFrame:
        with io.StringIO() as buf:
            buf.write(requests.get(self.url).text)
            buf.seek(0)
            return pd.read_csv(buf)


@dataclasses.dataclass
class TableQueryData:
    table_name: str
    filters: List[ColumnFilterData] = dataclasses.field(default_factory=list)

    @property
    def url_path(self):
        return f'/{self.table_name}' + ''.join(filter.url_path for filter in self.filters)


@dataclasses.dataclass
class ColumnFilterData:
    column_name: str
    operator: Literal['=', '!=', '<', '>', 'BEGINNING', 'CONTAINING']
    column_value: str

    @property
    def url_path(self):
        return f'/{self.column_name}/{self.operator}/{self.column_value}'
