from __future__ import annotations

import os

import pandas as pd

from db.company_names import CompanyAggregator
from db.connection import db
from db.envirofacts import Query
from db.models import CompanyModel, EmissionsModel


def create_tables():
    db.drop_all()
    db.create_all()


def fetch_envirofacts_data() -> pd.DataFrame:
    # We exclude Sector ID 17 because it corresponds to CO2
    # injection, and therefore those rows report negative emissions
    return (
        Query("pub_dim_facility")
        .table("pub_facts_sector_ghg_emission")
        .column_nequals("sector_id", "17")
        .get(fmt="json", pagesize=1000)
    )


def pull_envirofacts_data(file_path: str):
    fetch_envirofacts_data().to_csv(file_path, index=False)


def load_envirofacts_data(csv_file: str | None = None):
    if csv_file:
        if not os.path.exists(csv_file):
            pull_envirofacts_data(csv_file)
        data = pd.read_csv(csv_file)
    else:
        data = fetch_envirofacts_data()

    grouped_data = clean_envirofacts_data(data)

    for company_name in grouped_data.index.unique(level=0):
        emissions = [
            EmissionsModel(
                year=row.Index,
                facility_count=row.facility_count,
                all_facility_emissions=row.all_facility_emissions,
                fully_owned_emissions=row.fully_owned_emissions,
            )
            for row in grouped_data.loc[company_name].itertuples()
        ]
        company = CompanyModel(name=company_name, emissions=emissions)
        db.session.add(company)

    db.session.commit()


def clean_envirofacts_data(data: pd.DataFrame) -> pd.DataFrame:
    # Extract company names and their ownership stakes from the list
    # given in the parent_company column
    companies = (
        data.parent_company.str.split(r";\s*", regex=True, expand=True)
        .stack()
        .reset_index(level=1, drop=True)
        .str.extract(r"\s*(?P<company>.+)\s+\((?P<ownership>[0-9\.]+)%\)")
    )

    # Clean company names
    companies.company = pd.Series(
        CompanyAggregator.of(companies.company).aggregate(), index=companies.index
    )
    # Convert percentage to decimal
    companies.ownership = companies.ownership.astype(float) / 100

    # Down-select to only the columns we need, join with company data to get a unique
    # row for each facility/year/company pair
    data = data[["co2e_emission", "year"]].join(companies).reset_index(drop=True)
    # Some rows don't have company data; we exclude them
    data = data[~data.ownership.isnull()]
    # Calculate facility emissions normalized by ownership
    data["co2e_emission_owned"] = data.co2e_emission * data.ownership

    # Group data by company and year and aggregate the
    # statistics we want to save
    grouped_data = data.groupby(by=["company", "year"]).agg(
        facility_count=("co2e_emission", "count"),
        all_facility_emissions=("co2e_emission", "sum"),
        fully_owned_emissions=("co2e_emission_owned", "sum"),
    )
    # Drop companies whose facilities didn't report emissions
    grouped_data = grouped_data.loc[grouped_data.facility_count != 0]
    return grouped_data
