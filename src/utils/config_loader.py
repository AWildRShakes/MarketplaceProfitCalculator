# src/utils/config_loader.py
import json
import os
from typing import Dict
from ..models.fee import Fee, FeeType, FeeApplication
from ..models.marketplace import Marketplace, SellerTier
from ..models.shipping import ShippingCarrier, ShippingService, ShippingRate

class ConfigLoader:
    @staticmethod
    def load_marketplace(file_path: str) -> Marketplace:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        tiers = {}
        for tier_id, tier_data in data["tiers"].items():
            fees = {}
            for fee_id, fee_data in tier_data["fees"].items():
                fee_type = FeeType.COMPOUND if "percentage" in fee_data else \
                          FeeType.PERCENTAGE if fee_data["type"] == "percentage" else \
                          FeeType.FLAT
                
                fees[fee_id] = Fee(
                    type=fee_type,
                    application=FeeApplication(fee_data["application"]),
                    percentage=fee_data.get("percentage"),
                    flat_fee=fee_data.get("flat_fee", 0)
                )
            
            tiers[tier_id] = SellerTier(
                name=tier_data["name"],
                fees=fees
            )
        
        return Marketplace(
            name=data["name"],
            tiers=tiers
        )

    @staticmethod
    def load_shipping(file_path: str) -> ShippingCarrier:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        services = {}
        for service_id, service_data in data["services"].items():
            rates = [
                ShippingRate(
                    weight_up_to=rate_data["weight_up_to"],
                    price=rate_data["price"]
                )
                for rate_data in service_data["rates"]
            ]
            
            services[service_id] = ShippingService(
                name=service_data["name"],
                weight_limits=service_data["weight_limits"],
                rates=rates
            )
        
        return ShippingCarrier(
            name=data["name"],
            services=services
        )