 # src/models/fee.py
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Union, Dict

class FeeType(Enum):
    PERCENTAGE = auto()
    FLAT = auto()
    COMPOUND = auto()

class FeeApplication(Enum):
    PER_ITEM = "per_item"
    PER_ORDER = "per_order"

@dataclass
class Fee:
    type: FeeType
    application: FeeApplication
    percentage: Optional[float] = None
    flat_fee: Optional[float] = None

    def calculate(self, base_amount: float, quantity: int = 1) -> float:
        if self.type == FeeType.PERCENTAGE:
            fee = base_amount * (self.percentage / 100)
        elif self.type == FeeType.FLAT:
            fee = self.flat_fee
        else:  # COMPOUND
            fee = (base_amount * (self.percentage / 100)) + self.flat_fee

        if self.application == FeeApplication.PER_ITEM:
            return fee * quantity
        return fee