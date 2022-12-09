from __future__ import annotations

import dataclasses
import io
import logging
import sys
import time
from typing import Iterable, List, Literal

import pandas as pd
import requests
from flask import current_app, has_app_context

ENVIROFACTS_URL = "https://data.epa.gov/efservice"


def LOGGER() -> logging.Logger:
    if has_app_context():
        return current_app.logger
    return logging.getLogger


class Query:
    """
    A slapdash DSL for querying the
    [Envirofacts Data Service API](https://www.epa.gov/enviro/envirofacts-data-service-api)

    This API can be unreliable in unpredictable ways, so the general use of
    this interface is discouraged. The data this application needs has been
    pulled and saved at emissions-bot/csvdata/envirofacts_data.csv.
    """

    tables: List[TableQueryData]

    def __init__(self, table_name: str | None = None):
        self.tables = list()
        if table_name:
            self.tables.append(TableQueryData(table_name))

    @property
    def base_url(self) -> str:
        return ENVIROFACTS_URL + "".join(table.url_path for table in self.tables)

    def count(self) -> int:
        url = self.base_url + "/count/json"
        response = requests.get(url)
        response.raise_for_status()
        # The JSON keys returned by this query have inconsistent
        # capitalization, so we destructure the data positionally
        return int(list(response.json()[0].values())[0])

    def url(self, start=None, end=None, fmt: Literal["json", "csv"] = "json") -> str:
        rows = (
            "/rows/%s:%s" % (start, end)
            if (start is not None and end is not None)
            else ""
        )
        return self.base_url + rows + f"/{fmt}"

    def table(self, table_name: str):
        self.tables.append(TableQueryData(table_name))
        return self

    def column_equals(self, column_name: str, column_value: str):
        self.tables[-1].filters.append(
            ColumnFilterData(
                column_name=column_name, operator="=", column_value=column_value
            )
        )
        return self

    def column_nequals(self, column_name: str, column_value: str):
        self.tables[-1].filters.append(
            ColumnFilterData(
                column_name=column_name, operator="!=", column_value=column_value
            )
        )
        return self

    def column_less(self, column_name: str, column_value: str):
        self.tables[-1].filters.append(
            ColumnFilterData(
                column_name=column_name, operator="<", column_value=column_value
            )
        )
        return self

    def column_greater(self, column_name: str, column_value: str):
        self.tables[-1].filters.append(
            ColumnFilterData(
                column_name=column_name, operator=">", column_value=column_value
            )
        )
        return self

    def column_begins(self, column_name: str, column_value: str):
        self.tables[-1].filters.append(
            ColumnFilterData(
                column_name=column_name, operator="BEGINNING", column_value=column_value
            )
        )
        return self

    def column_contains(self, column_name: str, column_value: str):
        self.tables[-1].filters.append(
            ColumnFilterData(
                column_name=column_name,
                operator="CONTAINING",
                column_value=column_value,
            )
        )
        return self

    def get(
        self, pagesize: int | None = None, fmt: Literal["json", "csv"] = "json"
    ) -> pd.DataFrame:
        def url_to_df(_url: str, _fmt: Literal["json", "csv"]) -> pd.DataFrame:
            try:
                response = requests.get(_url)
                response.raise_for_status()
            except (requests.exceptions.HTTPError, ValueError):
                # Retry once on any failure
                time.sleep(5)
                response = requests.get(_url)
                response.raise_for_status()
            with io.StringIO() as buf:
                buf.write(response.text)
                buf.seek(0)
                try:
                    if _fmt == "json":
                        df = pd.read_json(buf, typ="frame")
                    else:
                        df = pd.read_csv(buf)
                except Exception:
                    LOGGER().error(
                        'Ill-formed data received from URL "%s": %s',
                        _url,
                        response.text,
                        sys.exc_info(),
                    )
                    raise
            LOGGER().info(
                'Successfully pulled %s rows and %s columns of data from URL "%s".',
                df.shape[0],
                df.shape[1],
                _url,
            )
            return df

        def get_page(
            _start: int, _end: int, _fmt: Literal["json", "csv"]
        ) -> pd.DataFrame:
            url = self.url(start=_start, end=_end, fmt=_fmt)
            return url_to_df(url, _fmt)

        fallback_fmt = "csv" if fmt == "json" else "json"

        if pagesize is not None:
            count = self.count()

            def pagegen() -> Iterable[pd.DataFrame]:
                for i in range(0, count, pagesize):
                    # Envirofact's row indices begin at 0, and row queries are both start-inclusive and end-inclusive
                    start = i
                    end = i + pagesize - 1

                    # If one format fails inexplicably for a certain page (which happens), we try the other
                    try:
                        yield get_page(start, end, fmt)
                    except (requests.exceptions.HTTPError, ValueError):
                        yield get_page(start, end, fallback_fmt)

            return pd.concat(pagegen(), ignore_index=True)

        else:
            return url_to_df(self.url(fmt=fmt), fmt)


@dataclasses.dataclass
class TableQueryData:
    table_name: str
    filters: List[ColumnFilterData] = dataclasses.field(default_factory=list)

    @property
    def url_path(self):
        return f"/{self.table_name}" + "".join(
            filter.url_path for filter in self.filters
        )


@dataclasses.dataclass
class ColumnFilterData:
    column_name: str
    operator: Literal["=", "!=", "<", ">", "BEGINNING", "CONTAINING"]
    column_value: str

    @property
    def url_path(self):
        return f"/{self.column_name}/{self.operator}/{self.column_value}"
