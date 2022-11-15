import os
import re
import zipfile
from typing import Generator, List

import pandas as pd

from emissions_bot import envirofacts
from emissions_bot.database import CompanyModel, EmissionsModel


def get_company_names() -> List[str]:
    facilities = envirofacts.Query('pub_dim_facility').get(usecols=['PARENT_COMPANY'])

    companies = set()
    for entry in facilities.PARENT_COMPANY:
        if pd.isnull(entry):
            continue
        separated = re.split(r'\s*\([0-9\.]+\%\);?\s*', entry)
        companies.update(company.upper() for company in separated[:-1])
    return sorted(companies)


def pull_company(company_name: str) -> CompanyModel:
    emissions: List[EmissionsModel] = list()

    data = envirofacts.Query('pub_dim_facility')\
        .column_contains('parent_company', company_name)\
        .table('pub_facts_sector_ghg_emission')\
        .column_nequals('sector_id', '17')\
        .get(usecols=['year', 'parent_company', 'co2e_emission'])
    pat = re.escape(company_name) + r'\s*\(([0-9\.]+)\%\)'
    ownership_coeff = data.parent_company.str.extract(pat, flags=re.IGNORECASE, expand=False).astype(float) / 100
    data['co2e_emission_owned'] = data.co2e_emission * ownership_coeff
    data = data[~ownership_coeff.isnull()]

    for row in data.groupby(by='year').aggregate(
        facility_count=('co2e_emission', 'count'),
        all_facility_emissions=('co2e_emission', 'sum'),
        fully_owned_emissions=('co2e_emission_owned', 'sum')
    ).itertuples():
        emissions.append(EmissionsModel(
            year=row.Index,
            facility_count=row.facility_count,
            all_facility_emissions=row.all_facility_emissions,
            fully_owned_emissions=row.fully_owned_emissions
        ))

    return CompanyModel(name=company_name, emissions=emissions)


def read_zip_data() -> pd.DataFrame:
    def df_gen() -> Generator[None, None, pd.DataFrame]:
        zip_path = os.path.abspath(os.path.join(__file__, '../../../envirofacts_data.zip'))
        with zipfile.ZipFile(zip_path) as zipf:
            for filename in zipf.namelist():
                if os.path.splitext(filename)[1] == '.json' and '__MACOSX' not in filename:
                    with zipf.open(filename) as f:
                        yield pd.read_json(f, orient='records')
    return pd.concat(df_gen(), ignore_index=True)


def pulled_data_to_company_model(data: pd.DataFrame) -> Generator[None, None, CompanyModel]:
    companies = data.parent_company\
        .str.split(r';\s*', regex=True, expand=True)\
        .stack()\
        .reset_index(level=1, drop=True)\
        .str.upper()\
        .str.extract(r'\s*(?P<company>.+)\s+\((?P<ownership>[0-9\.]+)%\)')
    companies.ownership = companies.ownership.astype(float) / 100

    data = data[['co2e_emission', 'year']].join(companies).reset_index(drop=True)
    data = data[~data.ownership.isnull()]
    data['co2e_emission_owned'] = data.co2e_emission * data.ownership

    grouped_data = data.groupby(by=['company', 'year']).agg(
        facility_count=('co2e_emission', 'count'),
        all_facility_emissions=('co2e_emission', 'sum'),
        fully_owned_emissions=('co2e_emission_owned', 'sum')
    )

    for company_name in grouped_data.index.levels[0]:
        emissions = [
            EmissionsModel(
                year=row.Index,
                facility_count=row.facility_count,
                all_facility_emissions=row.all_facility_emissions,
                fully_owned_emissions=row.fully_owned_emissions
            ) for row in grouped_data.loc[company_name].itertuples()
        ]
        yield CompanyModel(name=company_name, emissions=emissions)
