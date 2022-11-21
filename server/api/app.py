from apiflask import APIFlask, pagination_builder
from flask.cli import AppGroup

from api.facts import get_fact_template
from api.schemas import (CompanyListOutput, CompanyOutput, CompanyQueryInput,
                         EmissionComparisonFactOutput, EmissionFactQueryInput)
from db import CompanyModel, EmissionsModel, db, envirofacts_pipeline

app = APIFlask(__name__, openapi_blueprint_url_prefix='/api')
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI='postgresql+pg8000://',
)
db.init_app(app)

db_cli = AppGroup('db')
db_cli.command('init')(envirofacts_pipeline)
app.cli.add_command(db_cli)

app.logger.setLevel('INFO')


@app.get('/api/companies/<int:company_id>')
@app.output(CompanyOutput)
def get_company(company_id):
    return CompanyModel.query.get_or_404(company_id)


@app.get('/api/companies')
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


@app.get('/api/emissionComparisonFact')
@app.input(EmissionFactQueryInput, location='query')
@app.output(EmissionComparisonFactOutput)
def get_emission_comparison_fact(query):
    fact_template, next_shuffle_key = get_fact_template(query.get('shuffle_key'))
    return {
        'fact': fact_template.get_fact(query['emission']),
        'next_shuffle_key': next_shuffle_key
    }
