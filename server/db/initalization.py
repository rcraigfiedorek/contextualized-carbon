import re

import cleanco

from db.envirofacts import Query
from db.connection import db
from db.models import CompanyModel, EmissionsModel


def create_tables():
    db.drop_all()
    db.create_all()


def pull_envirofacts_data():
    data = Query('pub_dim_facility')\
        .table('pub_facts_sector_ghg_emission')\
        .get(fmt='json', pagesize=1000)

    companies = data.parent_company\
        .str.split(r';\s*', regex=True, expand=True)\
        .stack()\
        .reset_index(level=1, drop=True)\
        .str.upper()\
        .str.extract(r'\s*(?P<company>.+)\s+\((?P<ownership>[0-9\.]+)%\)')

    def cleanse_company_name(name):
        name = re.sub(r'(\([^\(\)]*(\)|$))(\[[^\[\]]*(\]|$))|,|\.', '', name)
        return cleanco.basename(name)

    companies.company = companies.company.map(cleanse_company_name, na_action='ignore')
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
        company = CompanyModel(name=company_name, emissions=emissions)
        db.session.add(company)

    db.session.commit()
