from apiflask import APIBlueprint, pagination_builder

from api.schemas import (CompanyListOutput, CompanyOutput, CompanyQueryInput,
                         EmissionComparisonFactOutput, EmissionFactQueryInput)
from db import CompanyModel, EmissionsModel

bp = APIBlueprint('api', __name__, url_prefix='/api')


@bp.get('/companies/<int:company_id>')
@bp.output(CompanyOutput)
def get_company(company_id):
    return CompanyModel.query.get_or_404(company_id)


@bp.get('/companies')
@bp.input(CompanyQueryInput, location='query')
@bp.output(CompanyListOutput)
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


@bp.get('/randomEmissionComparisonFact')
@bp.input(EmissionFactQueryInput, location='query')
@bp.output(EmissionComparisonFactOutput)
def get_random_emission_comparison_fact(query):
    return {}
