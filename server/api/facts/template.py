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
            numerical_result = self.tco2_conversion / tco2e
        else:
            numerical_result = self.tco2_conversion * tco2e
        return self.message % (numerical_result)
