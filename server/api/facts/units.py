from __future__ import annotations

import dataclasses
import itertools
from typing import ClassVar, Dict, Iterable

import numpy as np
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


ureg.define('trillionth = 1 / 1_000_000_000_000')
ureg.define('billionth = 1 / 1_000_000_000')
ureg.define('millionth = 1 / 1_000_000')
ureg.define('thousandth = 1 / 1_000')
ureg.define('one = 1')
ureg.define('thousand = 1_000')
ureg.define('million = 1_000_000')
ureg.define('billion = 1_000_000_000')
ureg.define('trillion = 1_000_000_000_000')


@dataclasses.dataclass
class PrettyUnit:
    unit: Unit
    pname_s: str | None = None  # pname_s is set to None only for the dimensionless unit
    pname_pl: str | None = None  # pname_pl defaults to f'{self.pname_pl}s' if not given
    threshold: float | None = None  # The fallback unit will be used as the threshold if none is given
    fallback_punit: PrettyUnit | None = None

    unitless: ClassVar[PrettyUnit]

    def __post_init__(self):
        if self.pname_pl is None and self.pname_s is not None:
            self.pname_pl = f'{self.pname_s}s'

    @staticmethod
    def of(*args) -> PrettyUnit:
        return PrettyUnit.of_iter(args)

    @staticmethod
    def of_iter(chain: Iterable[PrettyUnit]) -> PrettyUnit:
        first = None
        for punit, fallback in itertools.pairwise(chain):
            if first is None:
                first = punit
            punit.fallback_punit = fallback
        if first is None:
            raise ValueError('Expected non-empty iterable')
        return first

    def pformat(self, q: Quantity) -> str:
        m = q.to(self.unit).m
        if self.fallback_punit is not None:
            if self.threshold is not None:
                if (m >= self.threshold):
                    return self.fallback_punit.pformat(q)
            else:
                if (q >= (1 * self.fallback_punit.unit)):
                    return self.fallback_punit.pformat(q)
        if 0.1 <= m < 1_000:
            formatted_number = np.format_float_positional(m, precision=2, min_digits=2)
            use_plural = True
        else:
            formatted_number = PrettyUnit.unitless.pformat(m * ureg.one)
            use_plural = 'of a' not in formatted_number

        if self.pname_s is None or self.pname_pl is None:
            return formatted_number
        else:
            return f'{formatted_number} {self.pname_pl if use_plural else self.pname_s}'


PrettyUnit.unitless = PrettyUnit.of(
    PrettyUnit(ureg.trillionth, 'trillionth of a', 'trillionths of a'),
    PrettyUnit(ureg.billionth, 'billionth of a', 'billionths of a'),
    PrettyUnit(ureg.millionth, 'millionth of a', 'millionths of a'),
    PrettyUnit(ureg.thousandth, 'thousandth of a', 'thousandths of a'),
    PrettyUnit(ureg.one),
    PrettyUnit(ureg.thousand, 'thousand', 'thousands of'),
    PrettyUnit(ureg.million, 'million', 'millions of'),
    PrettyUnit(ureg.billion, 'billion', 'billions of'),
    PrettyUnit(ureg.trillion, 'trillion', 'trillions of')
)


PFORMAT_SUPPORTED_DIMENSIONS: Dict[pint.util.UnitsContainer, PrettyUnit] = {
    ureg.UnitsContainer({}):
        PrettyUnit.unitless,
    ureg.UnitsContainer({'[temperature]': 1}):
        PrettyUnit(ureg.delta_degC, 'degree Celsius', 'degrees Celsius'),
    ureg.UnitsContainer({'[time]': 1}): PrettyUnit.of(
        PrettyUnit(ureg.ns, 'nanosecond'),
        PrettyUnit(ureg.microsecond, 'microsecond'),
        PrettyUnit(ureg.ms, 'millisecond'),
        PrettyUnit(ureg.s, 'second'),
        PrettyUnit(ureg.min, 'minute'),
        PrettyUnit(ureg.hr, 'hour'),
        PrettyUnit(ureg.day, 'day'),
        PrettyUnit(ureg.year, 'year'),
        PrettyUnit(ureg.millennium, 'millennium', 'millennia')
    ),
    ureg.UnitsContainer({'[length]': 2}): PrettyUnit.of(
        PrettyUnit(ureg.mm ** 2, 'square millimeter'),
        PrettyUnit(ureg.cm ** 2, 'square centimeter', threshold=1000),
        PrettyUnit(ureg.m ** 2, 'square meter', threshold=1000),
        PrettyUnit(ureg.acre, 'acre'),
        PrettyUnit(ureg.hectare, 'hectare'),
        PrettyUnit(ureg.km ** 2, 'square kilometer')
    ),
    ureg.UnitsContainer({'[length]': 3}): PrettyUnit.of(
        PrettyUnit(ureg.microliter, 'microliter'),
        PrettyUnit(ureg.mL, 'milliliter'),
        PrettyUnit(ureg.L, 'liter'),
        PrettyUnit(ureg.km ** 3, 'cubic kilometer')
    ),
    ureg.UnitsContainer({'[mass]': 1}): PrettyUnit.of(
        PrettyUnit(ureg.mg, 'milligram'),
        PrettyUnit(ureg.g, 'gram'),
        PrettyUnit(ureg.kg, 'kilogram'),
        PrettyUnit(ureg.t, 'tonne'),
        PrettyUnit(ureg.kilotonne, 'kilotonne'),
        PrettyUnit(ureg.Mt, 'megatonne'),
        PrettyUnit(ureg.Gt, 'gigatonne')
    )
}


def pformat(q: Quantity | str) -> str:
    d = q.dimensionality
    if d not in PFORMAT_SUPPORTED_DIMENSIONS:
        raise ValueError(f'Unsupported dimensionality: {d}')
    return PFORMAT_SUPPORTED_DIMENSIONS[d].pformat(q)


def format_quantity_string(q: str) -> str:
    parsed = Quantity(q)
    return pformat(parsed)
