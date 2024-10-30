# src/models/fee.py
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Union, Dict
from src.utils.logger import Logger

logger = Logger.get_logger()

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

    def __post_init__(self):
        logger.debug(f"Created Fee object: type={self.type}, application={self.application}, "
                    f"percentage={self.percentage}, flat_fee={self.flat_fee}")
        self._validate()

    def _validate(self):
        if self.type == FeeType.PERCENTAGE and self.percentage is None:
            logger.error("Percentage fee created without percentage value")
            raise ValueError("Percentage fee requires a percentage value")
        
        if self.type == FeeType.FLAT and self.flat_fee is None:
            logger.error("Flat fee created without flat fee value")
            raise ValueError("Flat fee requires a flat fee value")
        
        if self.type == FeeType.COMPOUND and (self.percentage is None or self.flat_fee is None):
            logger.error("Compound fee created without required values")
            raise ValueError("Compound fee requires both percentage and flat fee values")

    def calculate(self, base_amount: float, quantity: int = 1) -> float:
        logger.debug(f"Calculating fee for base_amount={base_amount}, quantity={quantity}")
        
        try:
            if self.type == FeeType.PERCENTAGE:
                fee = base_amount * (self.percentage / 100)
                logger.debug(f"Calculated percentage fee: {fee}")
            elif self.type == FeeType.FLAT:
                fee = self.flat_fee
                logger.debug(f"Applied flat fee: {fee}")
            else:  # COMPOUND
                fee = (base_amount * (self.percentage / 100)) + self.flat_fee
                logger.debug(f"Calculated compound fee: {fee} "
                           f"(percentage={base_amount * (self.percentage / 100)}, "
                           f"flat={self.flat_fee})")

            if self.application == FeeApplication.PER_ITEM:
                final_fee = fee * quantity
                logger.debug(f"Applied per-item multiplication: {final_fee}")
            else:
                final_fee = fee
                logger.debug("Fee applied per order, no quantity multiplication")

            return final_fee
            
        except Exception as e:
            logger.error(f"Error calculating fee: {str(e)}", exc_info=True)
            raise