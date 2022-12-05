import dataclasses
import operator
from typing import Callable, Optional

from api.facts.quantity import Quantity, pformat, ureg


@dataclasses.dataclass
class FactTemplate:
    conversion: Quantity
    message: str
    citation: Optional[dict] = None
    calc_function: Callable[[Quantity, Quantity], Quantity] = operator.mul

    def get_fact(self, tco2e: float) -> str:
        co2_quantity = tco2e * (ureg.t * ureg.co2)
        calc_result = self.calc_function(self.conversion, co2_quantity)
        return self.message % (pformat(calc_result))
