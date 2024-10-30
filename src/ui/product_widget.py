# src/ui/product_widget.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QGridLayout, QGroupBox)
from PyQt5.QtCore import pyqtSignal

class ProductWidget(QWidget):
    input_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Product Group
        product_group = QGroupBox("Product Details")
        product_layout = QGridLayout()
        
        # Sale price input
        product_layout.addWidget(QLabel("Sale Price ($):"), 0, 0)
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Enter sale price")
        self.price_input.textChanged.connect(self.input_changed.emit)
        product_layout.addWidget(self.price_input, 0, 1)
        
        # Quantity input
        product_layout.addWidget(QLabel("Quantity:"), 1, 0)
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Enter quantity")
        self.quantity_input.textChanged.connect(self.input_changed.emit)
        product_layout.addWidget(self.quantity_input, 1, 1)
        
        # Cost per item input
        product_layout.addWidget(QLabel("Cost per Item ($):"), 2, 0)
        self.cost_input = QLineEdit()
        self.cost_input.setPlaceholderText("Enter cost per item")
        self.cost_input.textChanged.connect(self.input_changed.emit)
        product_layout.addWidget(self.cost_input, 2, 1)
        
        product_group.setLayout(product_layout)
        layout.addWidget(product_group)
    
    def get_sale_price(self) -> float:
        try:
            return float(self.price_input.text())
        except ValueError:
            return 0.0
    
    def get_quantity(self) -> int:
        try:
            return int(self.quantity_input.text())
        except ValueError:
            return 0
    
    def get_cost_per_item(self) -> float:
        try:
            return float(self.cost_input.text())
        except ValueError:
            return 0.0
        
    def has_valid_inputs(self) -> bool:
        try:
            price = self.get_sale_price()
            quantity = self.get_quantity()
            cost = self.get_cost_per_item()
            return all([price > 0, quantity > 0, cost >= 0])
        except ValueError:
            return False