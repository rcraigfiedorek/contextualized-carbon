from __future__ import annotations

import dataclasses
import io
from typing import List, Literal

import pandas as pd
import requests

ENVIROFACTS_URL = 'https://data.epa.gov/efservice'


class Query:

    tables: List[TableQueryData]

    def __init__(self, table_name: str | None = None):
        self.tables = list()
        if table_name:
            self.tables.append(TableQueryData(table_name))

    @property
    def base_url(self) -> str:
        return ENVIROFACTS_URL + ''.join(table.url_path for table in self.tables)

    def count(self) -> int:
        url = self.base_url + '/count/json'
        response = requests.get(url)
        response.raise_for_status()
        return int(list(response.json()[0].values())[0])

    def url(self, start=None, end=None) -> str:
        rows = ('/rows/%s:%s' % (start, end)) if (start is not None and end is not None) else ''
        return self.base_url + rows + '/CSV'

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

    def get(self, paginate=False, **kwargs) -> pd.DataFrame:
        def url_to_df(_url):
            print(_url)
            response = requests.get(_url)
            response.raise_for_status()
            with io.StringIO() as buf:
                buf.write(response.text)
                buf.seek(0)
                return pd.read_csv(buf, **kwargs)

        if paginate:
            print(self.count())
            return pd.concat((
                url_to_df(self.url(start=i, end=i+999))
                for i in range(0, self.count(), 1000)
            ), ignore_index=True)
        else:
            return url_to_df(self.url())


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
