# src/ui/marketplace_widget.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QLineEdit, QGridLayout, QGroupBox)
from PyQt5.QtCore import pyqtSignal
from src.models.marketplace import Marketplace
from src.utils.logger import Logger

class MarketplaceWidget(QWidget):
    input_changed = pyqtSignal()
    
    def __init__(self, marketplaces: dict[str, Marketplace], parent=None):
        super().__init__(parent)
        self.marketplaces = marketplaces
        self.logger = Logger.get_logger()
        self.logger.info("Initializing MarketplaceWidget")
        self.logger.debug(f"Available marketplaces: {', '.join(marketplaces.keys())}")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Marketplace Selection Group
        marketplace_group = QGroupBox("Marketplace Settings")
        marketplace_layout = QGridLayout()
        
        # Marketplace dropdown
        marketplace_layout.addWidget(QLabel("Marketplace:"), 0, 0)
        self.marketplace_combo = QComboBox()
        self.marketplace_combo.addItems(self.marketplaces.keys())
        self.marketplace_combo.currentTextChanged.connect(self.update_seller_tiers)
        self.marketplace_combo.currentTextChanged.connect(self.input_changed.emit)
        marketplace_layout.addWidget(self.marketplace_combo, 0, 1)
        
        # Seller tier dropdown
        marketplace_layout.addWidget(QLabel("Seller Tier:"), 1, 0)
        self.tier_combo = QComboBox()
        self.tier_combo.currentTextChanged.connect(self.input_changed.emit)
        marketplace_layout.addWidget(self.tier_combo, 1, 1)
        
        marketplace_group.setLayout(marketplace_layout)
        layout.addWidget(marketplace_group)
        
        # Initialize seller tiers
        self.update_seller_tiers()
        self.logger.debug("MarketplaceWidget UI setup completed")
    
    def update_seller_tiers(self):
        marketplace_name = self.marketplace_combo.currentText()
        self.logger.debug(f"Updating seller tiers for marketplace: {marketplace_name}")
        
        self.tier_combo.clear()
        if marketplace_name in self.marketplaces:
            tiers = self.marketplaces[marketplace_name].tiers.keys()
            self.tier_combo.addItems(tiers)
            self.logger.debug(f"Added tiers: {', '.join(tiers)}")
        else:
            self.logger.warning(f"Invalid marketplace selected: {marketplace_name}")
    
    def get_selected_marketplace(self) -> str:
        marketplace = self.marketplace_combo.currentText()
        if not marketplace:
            self.logger.warning("No marketplace selected")
        return marketplace
    
    def get_selected_tier(self) -> str:
        tier = self.tier_combo.currentText()
        if not tier:
            self.logger.warning("No seller tier selected")
        return tier