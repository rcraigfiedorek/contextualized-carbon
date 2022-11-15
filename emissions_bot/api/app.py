import os
from random import Random

from apiflask import APIFlask, pagination_builder

from emissions_bot import db_setup
from emissions_bot.api.schemas import (CompanyListOutput, CompanyOutput,
                                       CompanyQueryInput,
                                       EmissionComparisonFactOutput,
                                       EmissionFactQueryInput)
from emissions_bot.database import CompanyModel, EmissionsModel, db

app = APIFlask(__name__)
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI='sqlite:///project.db',
    TESTING=(os.getenv('FLASK_TESTING') == 'true'),
    REFRESH_DATABASE=(os.getenv('REFRESH_DATABASE') == 'true')
)
db.init_app(app)


@app.before_first_request
def refresh_database():
    if app.config['REFRESH_DATABASE']:
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
            emissions2019 = EmissionsModel(
                year=2019,
                facility_count=Random(2019).randint(1, 100),
                all_facility_emissions=Random(2019).random(),
                fully_owned_emissions=Random(2019).random() / 2
            )
            company_only_2019 = CompanyModel(
                name='Company with 2019 emissions',
                emissions=[emissions2019]
            )
            db.session.add(company_only_2019)
            db.session.commit()
        else:
            data = db_setup.read_zip_data()
            db.session.add_all(db_setup.pulled_data_to_company_model(data))
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
