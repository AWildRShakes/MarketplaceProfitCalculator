from typing import Dict, List, Optional
from ..models.marketplace import Marketplace, SellerTier
from ..models.shipping import ShippingCarrier, ShippingService
from dataclasses import dataclass
from .logger import Logger

logger = Logger.get_logger()

@dataclass
class ProfitCalculationResult:
    gross_revenue: float
    total_marketplace_fees: float
    shipping_cost: float
    total_cost: float
    net_profit: float
    profit_margin: float
    fee_breakdown: Dict[str, float]

class ProfitCalculator:
    def __init__(self, marketplace: Marketplace, shipping_carrier: ShippingCarrier):
        self.marketplace = marketplace
        self.shipping_carrier = shipping_carrier
        self.logger = Logger.get_logger()

    def calculate_profit(
        self,
        sale_price: float,
        quantity: int,
        cost_per_item: float,
        weight_per_item: float,
        tier_id: str,
        shipping_service_id: str
    ) -> ProfitCalculationResult:
        try:
            # Input validation
            if not all([sale_price, quantity, cost_per_item, weight_per_item, tier_id, shipping_service_id]):
                self.logger.warning(f"Invalid input parameters: sale_price={sale_price}, quantity={quantity}, "
                                  f"cost_per_item={cost_per_item}, weight_per_item={weight_per_item}, "
                                  f"tier_id={tier_id}, shipping_service_id={shipping_service_id}")
                raise ValueError("All input parameters must have non-zero values")

            # Get the seller tier
            if tier_id not in self.marketplace.tiers:
                self.logger.error(f"Invalid tier_id: {tier_id}. Available tiers: {list(self.marketplace.tiers.keys())}")
                raise ValueError(f"Invalid tier_id: {tier_id}")
            tier = self.marketplace.tiers[tier_id]
            
            # Calculate gross revenue
            gross_revenue = sale_price * quantity
            self.logger.debug(f"Calculated gross revenue: ${gross_revenue:.2f}")
            
            # Calculate marketplace fees
            fee_breakdown = {}
            total_marketplace_fees = 0
            
            for fee_name, fee in tier.fees.items():
                fee_amount = fee.calculate(sale_price, quantity)
                fee_breakdown[fee_name] = fee_amount
                total_marketplace_fees += fee_amount
                self.logger.debug(f"Calculated {fee_name}: ${fee_amount:.2f}")

            # Calculate shipping cost
            if shipping_service_id not in self.shipping_carrier.services:
                self.logger.error(f"Invalid shipping_service_id: {shipping_service_id}. "
                                f"Available services: {list(self.shipping_carrier.services.keys())}")
                raise ValueError(f"Invalid shipping_service_id: {shipping_service_id}")
                
            shipping_service = self.shipping_carrier.services[shipping_service_id]
            total_weight = weight_per_item * quantity
            shipping_cost = shipping_service.get_rate(total_weight)
            
            if shipping_cost is None:
                self.logger.warning(f"No shipping rate found for weight: {total_weight}oz")
                shipping_cost = 0
            
            self.logger.debug(f"Calculated shipping cost: ${shipping_cost:.2f}")

            # Calculate total cost and profit
            total_cost = (cost_per_item * quantity) + total_marketplace_fees + shipping_cost
            net_profit = gross_revenue - total_cost
            profit_margin = (net_profit / gross_revenue) * 100 if gross_revenue > 0 else 0

            self.logger.debug(f"Final calculations: total_cost=${total_cost:.2f}, "
                            f"net_profit=${net_profit:.2f}, profit_margin={profit_margin:.2f}%")

            return ProfitCalculationResult(
                gross_revenue=gross_revenue,
                total_marketplace_fees=total_marketplace_fees,
                shipping_cost=shipping_cost,
                total_cost=total_cost,
                net_profit=net_profit,
                profit_margin=profit_margin,
                fee_breakdown=fee_breakdown
            )
            
        except Exception as e:
            self.logger.error(f"Error in calculate_profit: {str(e)}", exc_info=True)
            raise