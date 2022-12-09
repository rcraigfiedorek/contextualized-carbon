import operator
from typing import List

from api.facts.template import FactTemplate, SingleVarFactTemplate
from api.facts.units import ureg

ALL_FACTS: List[FactTemplate] = list()


TRANSIENT_CLIMATE_RESPONSE_TO_EMISSIONS = (
    1.65 * ureg.delta_degC / (ureg.Eg * ureg.carbon)
)
tcre_fact = SingleVarFactTemplate(
    conversion=TRANSIENT_CLIMATE_RESPONSE_TO_EMISSIONS,
    message="This alone will raise the mean global temperature by <b>%s</b>.",
)
ALL_FACTS.append(tcre_fact)

EMPIRE_STATE_BUILDING_MASS = 331_122 * ureg.t
EMPIRE_STATE_BUILDINGS_PER_CO2 = 1 / (EMPIRE_STATE_BUILDING_MASS * ureg.co2)
empire_state_fact = SingleVarFactTemplate(
    conversion=EMPIRE_STATE_BUILDINGS_PER_CO2,
    message=(
        "This amount of carbon dioxide has the same mass as <b>%s Empire State"
        " Buildings</b>."
    ),
)
ALL_FACTS.append(empire_state_fact)

TAYLOR_SWIFT_JET_EMISSIONS = 0.35 * ureg.t * ureg.co2 / ureg.mi
EARTH_EQUATOR_DISTANCE = 24_901 * ureg.mi
TAYLOR_CIRCUMNAVIGATIONS_PER_EMISSIONS = 1 / (
    TAYLOR_SWIFT_JET_EMISSIONS * EARTH_EQUATOR_DISTANCE
)
TAYLOR_YEARLY_CIRCUMNAVIGATIONS_PERIOD = (
    ureg.yr / TAYLOR_CIRCUMNAVIGATIONS_PER_EMISSIONS
)
taylor_jet_fact = SingleVarFactTemplate(
    conversion=TAYLOR_YEARLY_CIRCUMNAVIGATIONS_PERIOD,
    message=(
        "Taylor Swift would have to fly her private jet around the entire equator"
        " <b>once every %s</b> for an entire year to generate the same emissions."
    ),
    calc_function=operator.truediv,
)
ALL_FACTS.append(taylor_jet_fact)

HUMMER_EMISSIONS = 555 * ureg.g * ureg.co2 / ureg.mi
HIGHWAY_SPEED = 60 * ureg.mi / ureg.h
HUMMER_HIGHWAY_YEARS_PER_EMISSIONS = 1 / (HUMMER_EMISSIONS * HIGHWAY_SPEED * ureg.yr)
hummer_fact = SingleVarFactTemplate(
    conversion=HUMMER_HIGHWAY_YEARS_PER_EMISSIONS,
    message=(
        "This is equal to the emissions generated from "
        "<b>%s Hummer H3s</b> driving at 60mph nonstop for an entire year."
    ),
)
ALL_FACTS.append(hummer_fact)

ARCTIC_SEA_ICE_MELT_PER_EMISSIONS = 3 * ureg.m**2 / (ureg.t * ureg.co2)
arctic_sea_ice_fact = SingleVarFactTemplate(
    conversion=ARCTIC_SEA_ICE_MELT_PER_EMISSIONS,
    message=(
        "This amount of carbon alone will cause the melting of <b>%s of ice</b> in the"
        " Arctic."
    ),
)
ALL_FACTS.append(arctic_sea_ice_fact)

TROPICAL_FOREST_YEARLY_SEQURESTRATION = 11 * ureg.t * ureg.co2 / ureg.ha
TROPICAL_FOREST_AREA_PER_EMISSION = 1 / TROPICAL_FOREST_YEARLY_SEQURESTRATION
tropical_forest_fact = SingleVarFactTemplate(
    conversion=TROPICAL_FOREST_AREA_PER_EMISSION,
    message=(
        "It would take <b>%s of tropical forest</b> to absorb this amount of carbon per"
        " year from the atmosphere."
    ),
)
ALL_FACTS.append(tropical_forest_fact)

NEW_ENGLAND_FOREST_YEARLY_SEQURESTRATION = 0.5 * ureg.t * ureg.co2 / ureg.ha
NEW_ENGLAND_FOREST_AREA_PER_EMISSION = 1 / NEW_ENGLAND_FOREST_YEARLY_SEQURESTRATION
new_england_forest_fact = SingleVarFactTemplate(
    conversion=NEW_ENGLAND_FOREST_AREA_PER_EMISSION,
    message=(
        "It would take <b>%s of New England forest</b> to absorb "
        "this amount of carbon per year from the atmosphere."
    ),
)
ALL_FACTS.append(new_england_forest_fact)


EARTH_AIR_COLUMN_DENSITY = 1.009 * ureg.kg / ureg.cm**2
CO2_LETHAL_CONCENTRATION = 0.1 * ureg.g * ureg.co2 / ureg.g
# The below calculation is the solution to this equation:
# CO2_LETHAL_CONCENTRATION == AIR_COLUMN_LETHAL_CO2 / (EARTH_AIR_COLUMN_DENSITY + AIR_COLUMN_LETHAL_CO2 / ureg.co2)
LETHAL_CO2_PER_AIR_COLUMN = (
    EARTH_AIR_COLUMN_DENSITY
    * CO2_LETHAL_CONCENTRATION
    / (1 - CO2_LETHAL_CONCENTRATION / ureg.co2)
)
AIR_COLUMN_POISONED_PER_CO2 = 1 / LETHAL_CO2_PER_AIR_COLUMN
poisoned_area_fact = SingleVarFactTemplate(
    conversion=AIR_COLUMN_POISONED_PER_CO2,
    message=(
        "Releasing this amount of carbon dioxide into <b>%s of Earth's air "
        "column</b> would cause lethal carbon dioxide poisoning for all humans "
        "in this area."
    ),
)
ALL_FACTS.append(poisoned_area_fact)

SODA_CO2_CONCENTRATION = 7 * ureg.g * ureg.co2 / ureg.L
SODA_VOLUME_PER_CO2 = 1 / SODA_CO2_CONCENTRATION
soda_fact = SingleVarFactTemplate(
    conversion=SODA_VOLUME_PER_CO2,
    message=(
        "This amount of carbon dioxide could be used to make <b>%s</b> of carbonated"
        " water."
    ),
)
ALL_FACTS.append(soda_fact)

CCUS_GLOBAL_RATE = 44_000_000 * ureg.t * ureg.co2 / ureg.yr
CCUS_TIME_PER_CO2 = 1 / CCUS_GLOBAL_RATE
ccus_fact = SingleVarFactTemplate(
    conversion=CCUS_TIME_PER_CO2,
    message=(
        "Carbon Capture, Utilization, and Storage (CCUS) is often touted as a solution"
        " to carbon emissions reduction. Yet it would take <b>%s</b> for the entire"
        " planet's CCUS operations to capture this amount of carbon."
    ),
)
ALL_FACTS.append(ccus_fact)

DAC_GLOBAL_RATE = 10_000 * ureg.t * ureg.co2 / ureg.yr
DAC_TIME_PER_CO2 = 1 / DAC_GLOBAL_RATE
dac_fact = SingleVarFactTemplate(
    conversion=DAC_TIME_PER_CO2,
    message=(
        "Direct Air Capture (DAC) is often touted as a solution to carbon emissions"
        " reduction. Yet it would take <b>%s</b> for the entire planet's DAC operations"
        " to capture this amount of carbon."
    ),
)
ALL_FACTS.append(dac_fact)

CO2_DENSITY = 1.815 * ureg.kg * ureg.co2 / ureg.m**3
AREA_OF_CM_CARPET_PER_CO2 = 1 / (CO2_DENSITY * ureg.cm)
carpet_fact = SingleVarFactTemplate(
    conversion=AREA_OF_CM_CARPET_PER_CO2,
    message=(
        "This is enough carbon dioxide to cover <b>%s</b> of land "
        "with a centimeter-high carpet of pure carbon dioxide."
    ),
)
ALL_FACTS.append(carpet_fact)


DEATHS_PER_EMISSIONS = 2.26e-4 / (ureg.t * ureg.co2)
death_fact = SingleVarFactTemplate(
    conversion=DEATHS_PER_EMISSIONS,
    message=(
        "Current research estimates that these emissions alone will directly "
        "cause <b>%s human deaths</b>."
    ),
)
ALL_FACTS.append(death_fact)
