# src/models/shipping.py
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class ShippingRate:
    weight_up_to: float
    price: float

@dataclass
class ShippingService:
    name: str
    weight_limits: Dict[str, float]
    rates: List[ShippingRate]

    def get_rate(self, weight: float) -> Optional[float]:
        if weight < self.weight_limits["min"] or weight > self.weight_limits["max"]:
            return None
        
        for rate in sorted(self.rates, key=lambda x: x.weight_up_to):
            if weight <= rate.weight_up_to:
                return rate.price
        return None

@dataclass
class ShippingCarrier:
    name: str
    services: Dict[str, ShippingService]