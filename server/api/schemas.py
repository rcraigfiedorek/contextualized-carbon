from apiflask import PaginationSchema, Schema, fields
from marshmallow import ValidationError, pre_dump, validate, validates_schema


class BaseSchema(Schema):
    class Meta:
        strict = True
        ordered = True


class EmissionsYearOutput(BaseSchema):
    facility_count = fields.Integer(
        required=True,
        metadata={
            "description": (
                "Given a company and a year, this is the number of facilities that"
                " reported emissions to the EPA in that year in which the company has"
                " an ownership stake."
            )
        },
    )
    all_facility_emissions = fields.Float(
        required=True,
        metadata={
            "description": (
                "The sum of all emissions reported by facilities the company had an"
                " ownership stake in for the given year. Given in metric tonnes of"
                " CO<sub>2</sub> equivalent."
            )
        },
    )
    fully_owned_emissions = fields.Float(
        required=True,
        metadata={
            "description": (
                "The sum of all emissions reported by facilities the company had an"
                " ownership stake in for the given year, normalized by ownership"
                " percentage. Given in metric tonnes of CO<sub>2</sub> equivalent."
            )
        },
    )


class CompanyOutput(BaseSchema):
    name = fields.String(
        required=True,
        metadata={"description": "Name of the company, as reported to the EPA"},
    )
    id = fields.Integer(
        required=True,
        metadata={
            "description": (
                "This API's unique identifier for the company. Susceptible to change"
                " before v1.0.0."
            )
        },
    )
    emissions_by_year = fields.Dict(
        keys=fields.Integer(as_string=True),
        values=fields.Nested(EmissionsYearOutput()),
        required=True,
        metadata={
            "description": (
                "A mapping whose keys are years and whose values are this company's"
                " emissions data for that year"
            )
        },
    )

    @pre_dump
    def map_years(self, data, **kwargs):
        data.emissions_by_year = {
            emissions.year: emissions for emissions in data.emissions
        }
        return data


class CompanyListOutput(BaseSchema, PaginationSchema):
    companies = fields.List(
        fields.Nested(CompanyOutput()),
        required=True,
        metadata={"description": "A list of queried companies"},
    )


class PaginationInput(BaseSchema):
    page = fields.Integer(load_default=1)
    per_page = fields.Integer(load_default=40)


class CompanyQueryInput(PaginationInput):
    name = fields.String(
        metadata={
            "description": (
                "Filter to include only companies whose name contains this string."
                " Case-insensitive."
            )
        }
    )
    year = fields.Integer(
        metadata={
            "description": (
                "Filter to include only companies who reported emissions in this year"
            )
        }
    )
    sort_by = fields.String(
        validate=validate.OneOf(
            (
                "name",
                "facility_count",
                "all_facility_emissions",
                "fully_owned_emissions",
            )
        ),
        metadata={
            "description": (
                "Specifies what attribute to sort results by. If an attribute other"
                ' than "name" is selected, then the "sort_year" field is required.'
            )
        },
    )
    sort_year = fields.Integer(
        metadata={
            "description": (
                'Specifies which year the "sort_by" attribute should be collected from.'
            )
        }
    )

    @validates_schema
    def validate_sort_year(self, data, **kwargs):
        sort_by = data.get("sort_by")
        sort_year = data.get("sort_year")
        sort_by_values_needing_year = (
            "facility_count",
            "all_facility_emissions",
            "fully_owned_emissions",
        )
        if sort_year and sort_by not in sort_by_values_needing_year:
            raise ValidationError(
                "sort_year may only be specified when sort_by is one of"
                ' "facility_count", "all_facility_emissions", or'
                ' "fully_owned_emissions".'
            )
        if not sort_year and sort_by in sort_by_values_needing_year:
            raise ValidationError(
                "sort_year parameter is required for given sort_by value."
            )


class EmissionFactQueryInput(BaseSchema):
    emission = fields.Float(
        required=True,
        metadata={
            "description": (
                "Specifies a quantity of GHG emissions in metric tonnes of"
                " CO<sub>2</sub> equivalent."
            )
        },
    )
    shuffle_key = fields.Integer(
        required=False,
        metadata={
            "description": (
                "Optional. Use to obtain a deterministic shuffle order that doesn't"
                " repeat fact templates until all have been returned."
            )
        },
    )
    include_bold_tags = fields.Boolean(
        required=False,
        load_default=False,
        metadata={
            "description": (
                "If true, the output text will include HTML tags for text emphasis."
            )
        },
    )


class EmissionComparisonFactOutput(BaseSchema):
    fact = fields.String(
        required=True,
        metadata={
            "description": (
                "A text fact comparing the specified emissions to another action of"
                " equivalent impact."
            )
        },
    )
    current_shuffle_key = fields.Integer(
        required=True,
        metadata={
            "description": (
                "The shuffle key that was used to select the output fact. If a shuffle"
                " key was specified as input, then this will be identical."
            )
        },
    )
    next_shuffle_key = fields.Integer(
        required=True,
        metadata={
            "description": (
                "The next shuffle key to use in order to maintain the backend's shuffle"
                " order."
            )
        },
    )
    citations = fields.List(
        fields.String(),
        dump_default=list,
        required=True,
        metadata={
            "description": (
                "A list of citations for the information given in the fact. Currently"
                ' omitted -- sources may be found at <a rel="noopener noreferrer"'
                ' target="_blank"'
                ' href="https://github.com/rcraigfiedorek/emissions-bot/blob/main/SOURCES.md">'
                "https://github.com/rcraigfiedorek/emissions-bot/blob/main/SOURCES.md</a>."
            )
        },
    )


class FormatQuantityQueryInput(BaseSchema):
    quantity = fields.String(
        require=True,
        metadata={"description": "A string containing a number and a unit"},
    )


class FormatQuantityOutput(BaseSchema):
    formatted_quantity = fields.String(
        require=True,
        metadata={
            "description": (
                "The input quantity, formatted to match the styles of the fact"
                " endpoint."
            )
        },
    )
