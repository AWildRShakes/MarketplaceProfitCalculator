# src/models/marketplace.py
from dataclasses import dataclass
from typing import Dict, List
from models.fee import Fee
from src.utils.logger import Logger

logger = Logger.get_logger()

@dataclass
class SellerTier:
    name: str
    fees: Dict[str, Fee]

    def __post_init__(self):
        logger.info(f"Created SellerTier: {self.name} with {len(self.fees)} fees")
        logger.debug(f"SellerTier fees: {', '.join(self.fees.keys())}")

@dataclass
class Marketplace:
    name: str
    tiers: Dict[str, SellerTier]

    def __post_init__(self):
        logger.info(f"Created Marketplace: {self.name} with {len(self.tiers)} tiers")
        logger.debug(f"Marketplace tiers: {', '.join(self.tiers.keys())}")