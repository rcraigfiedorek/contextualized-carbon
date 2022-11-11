from apiflask import PaginationSchema, Schema, fields
from marshmallow import pre_dump


class BaseSchema(Schema):
    class Meta:
        strict = True


class EmissionsYearOutput(BaseSchema):
    facility_count = fields.Integer(required=True)
    all_facility_emissions = fields.Float(required=True)
    fully_owned_emissions = fields.Float(required=True)


class CompanyOutput(BaseSchema):
    name = fields.String(required=True)
    id = fields.String(required=True)
    emissions_by_year = fields.Mapping(
        keys=fields.Integer(as_string=True),
        values=fields.Nested(EmissionsYearOutput()),
        required=True
    )

    @pre_dump
    def map_years(self, data, **kwargs):
        data.emissions_by_year = {
            emissions.year: emissions for emissions in data.emissions
        }
        return data


class CompanyListOutput(BaseSchema, PaginationSchema):
    companies = fields.List(fields.Nested(CompanyOutput()), required=True)


class PaginationInput(BaseSchema):
    page = fields.Integer(load_default=1)
    per_page = fields.Integer(load_default=40)


class EmissionQueryInput(BaseSchema):
    emission = fields.Float(required=True)


class EmissionComparisonFactOutput(BaseSchema):
    fact = fields.String(required=True)
    citations = fields.List(fields.String(), dump_default=list, required=True)


class RefreshDatabaseInput(BaseSchema):
    pass
