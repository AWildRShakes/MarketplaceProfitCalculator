# src/models/shipping.py
from dataclasses import dataclass
from typing import Dict, List, Optional
from src.utils.logger import Logger

logger = Logger.get_logger()

@dataclass
class ShippingRate:
    weight_up_to: float
    price: float

    def __post_init__(self):
        logger.debug(f"Created ShippingRate: weight_up_to={self.weight_up_to}, price={self.price}")

@dataclass
class ShippingService:
    name: str
    weight_limits: Dict[str, float]
    rates: List[ShippingRate]

    def __post_init__(self):
        logger.info(f"Created ShippingService: {self.name}")
        logger.debug(f"Weight limits: min={self.weight_limits['min']}, max={self.weight_limits['max']}")
        logger.debug(f"Number of rates: {len(self.rates)}")

    def get_rate(self, weight: float) -> Optional[float]:
        logger.debug(f"Getting shipping rate for weight: {weight}")
        
        if weight < self.weight_limits["min"] or weight > self.weight_limits["max"]:
            logger.warning(f"Weight {weight} is outside limits: "
                         f"min={self.weight_limits['min']}, max={self.weight_limits['max']}")
            return None
        
        for rate in sorted(self.rates, key=lambda x: x.weight_up_to):
            if weight <= rate.weight_up_to:
                logger.debug(f"Found applicable rate: {rate.price} for weight {weight}")
                return rate.price
                
        logger.warning(f"No applicable rate found for weight: {weight}")
        return None

@dataclass
class ShippingCarrier:
    name: str
    services: Dict[str, ShippingService]

    def __post_init__(self):
        logger.info(f"Created ShippingCarrier: {self.name} with {len(self.services)} services")
        logger.debug(f"Available services: {', '.join(self.services.keys())}")