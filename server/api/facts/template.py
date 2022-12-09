import dataclasses
import operator
import re
from typing import Callable, List, Optional

from api.facts.units import Quantity, pformat, ureg


@dataclasses.dataclass
class FactTemplate:
    conversions: List[Quantity]
    message: str
    calc_functions: List[Callable[[Quantity, Quantity], Quantity]] = None
    citation: Optional[dict] = None
    message_no_tags: str = None

    def __post_init__(self):
        if self.calc_functions is None:
            self.calc_functions = [operator.mul] * len(self.conversions)
        if self.message_no_tags is None:
            self.message_no_tags = re.sub(r"<.*?>", "", self.message)

    def get_fact(self, tco2e: float, include_bold_tags=False) -> str:
        co2_quantity = tco2e * (ureg.t * ureg.co2)
        template = self.message if include_bold_tags else self.message_no_tags
        return template % tuple(
            pformat(calc_function(conversion, co2_quantity))
            for calc_function, conversion in zip(self.calc_functions, self.conversions)
        )


def SingleVarFactTemplate(
    conversion: Quantity,
    message: str,
    calc_function: Callable[[Quantity, Quantity], Quantity] = operator.mul,
    citation: Optional[dict] = None,
) -> FactTemplate:
    return FactTemplate([conversion], message, [calc_function], citation)
