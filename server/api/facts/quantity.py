import pint

ureg = pint.UnitRegistry()
# The following is a bit of a hack to include carbon and carbon dioxide in unit calculations.
# We abuse the fact that 1 mole of carbon dioxide contains exactly 1 mole of carbon.
# If this were not the case, then we would need to be careful about atoms/molecule type conversions.
# These units are specified to fit the dimensional requirement [mass] * [carbon(_dioxide)] = [substance]
ureg.define('carbon = 1 / (12.011 g / mol) = C')
ureg.define('carbon_dioxide = 1 / (44.009 g / mol) = co2')
Quantity: type = ureg.Quantity
Unit: type = ureg.Unit


def pformat(q: Quantity) -> str:
    return str(q)
