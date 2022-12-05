from apiflask import PaginationSchema, Schema, fields
from marshmallow import ValidationError, pre_dump, validate, validates_schema


class BaseSchema(Schema):
    class Meta:
        strict = True
        ordered = True


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


class CompanyQueryInput(PaginationInput):
    name = fields.String()
    year = fields.Integer()
    sort_by = fields.String(validate=validate.OneOf((
        'name', 'facility_count', 'all_facility_emissions', 'fully_owned_emissions'
    )))
    sort_year = fields.Integer()

    @validates_schema
    def validate_sort_year(self, data, **kwargs):
        sort_by = data.get('sort_by')
        sort_year = data.get('sort_year')
        sort_by_values_needing_year = (
            'facility_count',
            'all_facility_emissions',
            'fully_owned_emissions'
        )
        if sort_year and sort_by not in sort_by_values_needing_year:
            raise ValidationError(
                'sort_year may only be specified when sort_by is one of '
                '"facility_count", "all_facility_emissions", or "fully_owned_emissions".'
            )
        if not sort_year and sort_by in sort_by_values_needing_year:
            raise ValidationError('sort_year parameter is required for given sort_by value.')


class EmissionFactQueryInput(BaseSchema):
    emission = fields.Float(required=True)
    shuffle_key = fields.Integer(required=False)


class EmissionComparisonFactOutput(BaseSchema):
    fact = fields.String(required=True)
    current_shuffle_key = fields.Integer(required=True)
    next_shuffle_key = fields.Integer(required=True)
    citations = fields.List(fields.String(), dump_default=list, required=True)
