# src/models/marketplace.py
from dataclasses import dataclass
from typing import Dict, List
from .fee import Fee

@dataclass
class SellerTier:
    name: str
    fees: Dict[str, Fee]

@dataclass
class Marketplace:
    name: str
    tiers: Dict[str, SellerTier]