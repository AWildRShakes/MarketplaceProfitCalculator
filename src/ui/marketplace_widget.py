# src/ui/marketplace_widget.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QLineEdit, QGridLayout, QGroupBox)
from PyQt5.QtCore import pyqtSignal
from src.models.marketplace import Marketplace

class MarketplaceWidget(QWidget):
    # Signal when any input changes
    input_changed = pyqtSignal()
    
    def __init__(self, marketplaces: dict[str, Marketplace], parent=None):
        super().__init__(parent)
        self.marketplaces = marketplaces
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
    
    def update_seller_tiers(self):
        marketplace_name = self.marketplace_combo.currentText()
        self.tier_combo.clear()
        if marketplace_name in self.marketplaces:
            self.tier_combo.addItems(self.marketplaces[marketplace_name].tiers.keys())
    
    def get_selected_marketplace(self) -> str:
        return self.marketplace_combo.currentText()
    
    def get_selected_tier(self) -> str:
        return self.tier_combo.currentText()