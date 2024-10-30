# src/utils/config_loader.py
import json
import os
from typing import Dict
from src.models.fee import Fee, FeeType, FeeApplication
from src.models.marketplace import Marketplace, SellerTier
from src.models.shipping import ShippingCarrier, ShippingService, ShippingRate
from src.utils.logger import Logger

class ConfigLoader:
    logger = Logger.get_logger()

    @staticmethod
    def load_marketplace(file_path: str) -> Marketplace:
        logger = ConfigLoader.logger
        logger.info(f"Loading marketplace configuration from: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                logger.debug(f"Successfully loaded JSON data from {file_path}")
            
            tiers = {}
            for tier_id, tier_data in data["tiers"].items():
                logger.debug(f"Processing tier: {tier_id}")
                fees = {}
                
                for fee_id, fee_data in tier_data["fees"].items():
                    logger.debug(f"Processing fee: {fee_id} for tier: {tier_id}")
                    
                    # Determine fee type and get appropriate values
                    if fee_data["type"] == "compound":
                        fee_type = FeeType.COMPOUND
                        percentage = fee_data.get("percentage")
                        flat_fee = fee_data.get("flat_fee")
                    elif fee_data["type"] == "percentage":
                        fee_type = FeeType.PERCENTAGE
                        percentage = fee_data.get("value")  # Changed from "percentage" to "value"
                        flat_fee = None
                    else:
                        fee_type = FeeType.FLAT
                        percentage = None
                        flat_fee = fee_data.get("value", 0)  # Also using "value" for flat fees
                    
                    logger.debug(f"Determined fee type: {fee_type} for fee: {fee_id}")
                    
                    try:
                        fees[fee_id] = Fee(
                            type=fee_type,
                            application=FeeApplication(fee_data["application"]),
                            percentage=percentage,
                            flat_fee=flat_fee
                        )
                    except ValueError as e:
                        logger.error(f"Error creating fee {fee_id}: {str(e)}")
                        raise
                
                tiers[tier_id] = SellerTier(
                    name=tier_data["name"],
                    fees=fees
                )
                logger.debug(f"Created tier {tier_id} with {len(fees)} fees")
            
            marketplace = Marketplace(
                name=data["name"],
                tiers=tiers
            )
            
            logger.info(f"Successfully loaded marketplace {marketplace.name} "
                       f"with {len(marketplace.tiers)} tiers")
            return marketplace
            
        except FileNotFoundError:
            logger.error(f"Marketplace configuration file not found: {file_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in marketplace configuration: {str(e)}")
            raise
        except KeyError as e:
            logger.error(f"Missing required field in marketplace configuration: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading marketplace configuration: {str(e)}", 
                        exc_info=True)
            raise

    @staticmethod
    def load_shipping(file_path: str) -> ShippingCarrier:
        logger = ConfigLoader.logger
        logger.info(f"Loading shipping configuration from: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                logger.debug(f"Successfully loaded JSON data from {file_path}")
            
            services = {}
            for service_id, service_data in data["services"].items():
                logger.debug(f"Processing shipping service: {service_id}")
                
                try:
                    rates = []
                    for rate_data in service_data["rates"]:
                        rate = ShippingRate(
                            weight_up_to=rate_data["weight_up_to"],
                            price=rate_data["price"]
                        )
                        rates.append(rate)
                        logger.debug(f"Added rate for weight up to {rate.weight_up_to}oz: "
                                   f"${rate.price}")
                    
                    services[service_id] = ShippingService(
                        name=service_data["name"],
                        weight_limits=service_data["weight_limits"],
                        rates=rates
                    )
                    
                    logger.debug(f"Created shipping service {service_id} with {len(rates)} rates")
                    
                except KeyError as e:
                    logger.error(f"Missing required field in service {service_id}: {str(e)}")
                    raise
            
            carrier = ShippingCarrier(
                name=data["name"],
                services=services
            )
            
            logger.info(f"Successfully loaded shipping carrier {carrier.name} "
                       f"with {len(carrier.services)} services")
            return carrier
            
        except FileNotFoundError:
            logger.error(f"Shipping configuration file not found: {file_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in shipping configuration: {str(e)}")
            raise
        except KeyError as e:
            logger.error(f"Missing required field in shipping configuration: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading shipping configuration: {str(e)}", 
                        exc_info=True)
            raise