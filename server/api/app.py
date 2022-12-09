import os

import click
from apiflask import APIFlask, pagination_builder
from flask.cli import AppGroup
from flask_cors import CORS

from api.facts import format_quantity_string, get_fact_template
from api.schemas import (
    CompanyListOutput,
    CompanyOutput,
    CompanyQueryInput,
    EmissionComparisonFactOutput,
    EmissionFactQueryInput,
    FormatQuantityOutput,
    FormatQuantityQueryInput,
)
from db import CompanyModel, EmissionsModel, create_tables, db, load_envirofacts_data

app = APIFlask(
    __name__,
    title="Corporate Emissions Facts API",
    version="0.0.1",
    openapi_blueprint_url_prefix="/api",
)
app.config.from_mapping(
    ENVIRONMENT=os.getenv("APP_ENV", "production"),
    DESCRIPTION=(
        "This is a free and public API that exposes sanitized corporate emissions data"
        ' sourced from the <a href="https://www.epa.gov/ghgreporting" target="_blank"'
        ' rel="noopener noreferrer">EPA Greenhouse Gas Reporting Program</a>. Functions'
        " that aid public comprehension of the magnitude of corporate emissions are"
        " also included."
    ),
    CONTACT={"name": "Craig Fiedorek", "email": "rcraigfiedorek@gmail.com"},
    LICENSE={
        "name": "GNU General Public License 3.0",
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
    },
    TAGS=["CorporateEmissionsFacts"],
)
if app.config["ENVIRONMENT"] == "development":
    CORS(origins=["http://localhost:3000"]).init_app(app)
db.init_app(app)


db_cli = AppGroup("db")
db_cli.command("create")(create_tables)
db_cli.command("seed")(
    click.argument("csv_file", required=False)(load_envirofacts_data)
)
app.cli.add_command(db_cli)


app.logger.setLevel("INFO")


@app.teardown_appcontext
def teardown_db(exception):
    db.session.close()


@app.get("/api/companies/<int:company_id>")
@app.output(CompanyOutput)
@app.doc(tags=["CorporateEmissionsFacts"])
def get_company(company_id):
    """
    Get a specific company's emissions data
    """
    return CompanyModel.query.get_or_404(company_id)


@app.get("/api/companies")
@app.input(CompanyQueryInput, location="query")
@app.output(CompanyListOutput)
@app.doc(tags=["CorporateEmissionsFacts"])
def get_companies(query):
    """
    Query a list of companies and get their emissions data
    """
    sql = CompanyModel.query
    if "name" in query:
        sql = sql.filter(CompanyModel.name.ilike(f'%{query["name"]}%'))
    if "year" in query:
        sql = sql.filter(
            CompanyModel.emissions.any(EmissionsModel.year == query["year"])
        )
    if "sort_by" in query:
        if query["sort_by"] == "name":
            sql = sql.order_by(CompanyModel.name)
        else:
            sql = (
                sql.join(CompanyModel.emissions)
                .filter(EmissionsModel.year == query["sort_year"])
                .order_by(getattr(EmissionsModel, query["sort_by"]).desc())
            )

    result = sql.paginate(page=query["page"], per_page=query["per_page"])
    return dict(companies=result.items, **pagination_builder(result))


@app.get("/api/emissionComparisonFact")
@app.input(EmissionFactQueryInput, location="query")
@app.output(EmissionComparisonFactOutput)
@app.doc(tags=["CorporateEmissionsFacts"])
def get_emission_comparison_fact(query):
    """
    Get a fact comparing an emission quantity to an action with equivalent impact.
    """
    fact_template, current_shuffle_key, next_shuffle_key = get_fact_template(
        query.get("shuffle_key")
    )
    return {
        "fact": fact_template.get_fact(
            query["emission"], include_bold_tags=query["include_bold_tags"]
        ),
        "current_shuffle_key": current_shuffle_key,
        "next_shuffle_key": next_shuffle_key,
    }


@app.get("/api/format-quantity")
@app.input(FormatQuantityQueryInput, location="query")
@app.output(FormatQuantityOutput)
@app.doc(tags=["CorporateEmissionsFacts"])
def get_formatted_quantity(query):
    """
    Utility method for formatting unitful data
    """
    return {"formatted_quantity": format_quantity_string(query["quantity"])}
