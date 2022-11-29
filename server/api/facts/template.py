import dataclasses
from typing import Optional


@dataclasses.dataclass
class ZeroDimensionalFactTemplate:
    tco2_conversion: float
    message: str
    citation: Optional[dict] = None
    invert_input: bool = False

    def get_fact(self, tco2e: float) -> str:
        if self.invert_input:
            try:
                numerical_result = self.tco2_conversion / tco2e
            except ZeroDivisionError:
                numerical_result = '__ZeroDivisionError__'
        else:
            numerical_result = self.tco2_conversion * tco2e
        return self.message % (numerical_result)
