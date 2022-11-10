from apiflask import APIFlask, Schema, fields

app = APIFlask(__name__)


class CompanyEmissionsYearOutput:
    company_name = fields.String()
    year = fields.Integer()
    facilityCount = fields.Integer()
    co2e_emission_all_facilities = fields.Float()
    co2e_emission_fully_owned = fields.Float()


class PaginatedSchema:
    offset = fields.Integer()
    limit = fields.Integer()
    total_results = fields.Integer()


class CompanyEmissionsYearListOutput(Schema, PaginatedSchema):
    companies = fields.List(fields.Nested(CompanyEmissionsYearOutput))


class PaginationParameters(Schema):
    offset = fields.Integer(load_default=0)
    limit = fields.Integer(load_default=40)


class EmissionQueryInput(Schema):
    emission = fields.Float(required=True)


class EmissionComparisonFactOutput(Schema):
    fact = fields.String()
    citations = fields.List(fields.String(), dump_default=list)


@app.route('/')
def hello_world():
    return '<p>Hello world!</p>'


@app.get('/companies')
@app.input(PaginationParameters, location='query')
@app.output(CompanyEmissionsYearListOutput)
def get_companies():
    return {}


@app.get('/randomEmissionComparisonFact')
@app.input(EmissionQueryInput, location='query')
@app.output(EmissionComparisonFactOutput)
def get_random_emission_comparison_fact():
    return {}
