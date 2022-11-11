import os
from random import Random

from apiflask import APIFlask, pagination_builder

from emissions_bot.api.schemas import (CompanyListOutput, CompanyOutput,
                                       EmissionComparisonFactOutput,
                                       EmissionQueryInput, PaginationInput,
                                       RefreshDatabaseInput)
from emissions_bot.database import CompanyModel, EmissionsModel, db

app = APIFlask(__name__)
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI='sqlite:///project.db',
    TESTING=(os.getenv('FLASK_TESTING') == 'true')
)
db.init_app(app)


@app.before_first_request
def build_database():
    db.drop_all()
    db.create_all()
    if app.config['TESTING']:
        for i in range(50):
            emissions2020 = EmissionsModel(
                year=2020,
                facility_count=Random(2020*i).randint(1, 100),
                all_facility_emissions=Random(2020*i).random(),
                fully_owned_emissions=Random(2020*i).random() / 2
            )
            emissions2021 = EmissionsModel(
                year=2021,
                facility_count=Random(2021*i).randint(1, 100),
                all_facility_emissions=Random(2021*i).random(),
                fully_owned_emissions=Random(2021*i).random() / 2
            )
            company = CompanyModel(
                name=f'Test Company {i}',
                emissions=[emissions2020, emissions2021]
            )
            db.session.add(company)
        db.session.commit()


@app.route('/')
def hello_world():
    return '<p>Hello world!</p>'


@app.get('/company/<int:company_id>')
@app.output(CompanyOutput)
def get_company(company_id):
    return CompanyModel.query.get_or_404(company_id)


@app.get('/companies')
@app.input(PaginationInput, location='query')
@app.output(CompanyListOutput)
def get_companies(query):
    result = CompanyModel.query.paginate(
        page=query['page'],
        per_page=query['per_page']
    )
    return dict(companies=result.items, **pagination_builder(result))


@app.get('/randomEmissionComparisonFact')
@app.input(EmissionQueryInput, location='query')
@app.output(EmissionComparisonFactOutput)
def get_random_emission_comparison_fact(query):
    return {}


@app.post('/refreshDatabase')
@app.input(RefreshDatabaseInput)
def refresh_database(body):
    return {}
