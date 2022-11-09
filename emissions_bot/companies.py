

import re
from typing import List

import pandas as pd

from emissions_bot.envirofacts import Query


def get_all_envirofacts_companies() -> List[str]:
    companies = set()
    for company_string in Query('pub_dim_facility').get().parent_company:
        if pd.isnull(company_string):
            continue
        separated_companies = re.split(r'\s*\([0-9\.]+\%\);?\s*', company_string)
        companies.update(company.casefold() for company in separated_companies[:-1])
    return sorted(companies)


class Company:

    name: str

    def __init__(self, name):
        self.name = name

    def get_all_facility_emissions_tco2(self, year='2021') -> float:
        """
        Sum of all reported emissions for facilities that this company has an ownership stake in
        """
        df = Query('pub_dim_facility')\
            .column_contains('parent_company', self.name)\
            .column_equals('year', year)\
            .table('pub_facts_sector_ghg_emission')\
            .column_nequals('sector_id', '17')\
            .get()
        return df.co2e_emission.sum()

    def get_normalized_facility_emissions_tco2(self, year='2021') -> float:
        """
        Sum of all reported emissions for facilities that this company owns, normalized by percent ownership
        """
        df = Query('pub_dim_facility')\
            .column_contains('parent_company', self.name)\
            .column_equals('year', year)\
            .table('pub_facts_sector_ghg_emission')\
            .column_nequals('sector_id', '17')\
            .get()
        pat = re.escape(self.name) + r'\s*\(([0-9.]+)\%\)'
        ownership_coeff = df.parent_company.str.extract(pat, flags=re.IGNORECASE, expand=False).astype(float) / 100
        return (df.co2e_emission * ownership_coeff).sum()
