import os
from random import Random

import click
from apiflask import APIFlask, pagination_builder
from flask.cli import AppGroup

from emissions_bot import db_setup
from emissions_bot.api.schemas import (CompanyListOutput, CompanyOutput,
                                       CompanyQueryInput,
                                       EmissionComparisonFactOutput,
                                       EmissionFactQueryInput)
from emissions_bot.database import (CompanyModel, EmissionsModel,
                                    Initalization, db)

app = APIFlask(__name__)
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI='sqlite:///project.db',
)
db.init_app(app)

db_cli = AppGroup('db')


@db_cli.command('init')
@click.argument('path')
def db_init(path):
    companies = Initalization(path).companies()
    db.session.add_all(companies)
    db.session.commit()


@app.route('/')
def hello_world():
    return '<p>Hello world!</p>'


@app.get('/companies/<int:company_id>')
@app.output(CompanyOutput)
def get_company(company_id):
    return CompanyModel.query.get_or_404(company_id)


@app.get('/companies')
@app.input(CompanyQueryInput, location='query')
@app.output(CompanyListOutput)
def get_companies(query):
    sql = CompanyModel.query
    if 'name' in query:
        sql = sql.filter(CompanyModel.name.ilike(f'%{query["name"]}%'))
    if 'year' in query:
        sql = sql.filter(CompanyModel.emissions.any(EmissionsModel.year == query['year']))
    if 'sort_by' in query:
        if query['sort_by'] == 'name':
            sql = sql.order_by(CompanyModel.name)
        else:
            sql = sql.join(CompanyModel.emissions)\
                .filter(EmissionsModel.year == query['sort_year'])\
                .order_by(getattr(EmissionsModel, query['sort_by']).desc())

    result = sql.paginate(
        page=query['page'],
        per_page=query['per_page']
    )
    return dict(companies=result.items, **pagination_builder(result))


@app.get('/randomEmissionComparisonFact')
@app.input(EmissionFactQueryInput, location='query')
@app.output(EmissionComparisonFactOutput)
def get_random_emission_comparison_fact(query):
    return {}
