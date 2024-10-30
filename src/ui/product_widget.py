# src/ui/product_widget.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QGridLayout, QGroupBox)
from PyQt5.QtCore import pyqtSignal
from src.utils.logger import Logger

class ProductWidget(QWidget):
    input_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = Logger.get_logger()
        self.logger.info("Initializing ProductWidget")
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
        self.logger.debug("ProductWidget UI setup completed")
    
    def get_sale_price(self) -> float:
        try:
            price = float(self.price_input.text())
            if price <= 0:
                self.logger.warning(f"Invalid sale price entered: {price}")
                return 0.0
            return price
        except ValueError:
            self.logger.warning(f"Invalid sale price format: {self.price_input.text()}")
            return 0.0
    
    def get_quantity(self) -> int:
        try:
            quantity = int(self.quantity_input.text())
            if quantity <= 0:
                self.logger.warning(f"Invalid quantity entered: {quantity}")
                return 0
            return quantity
        except ValueError:
            self.logger.warning(f"Invalid quantity format: {self.quantity_input.text()}")
            return 0
    
    def get_cost_per_item(self) -> float:
        try:
            cost = float(self.cost_input.text())
            if cost < 0:
                self.logger.warning(f"Invalid cost entered: {cost}")
                return 0.0
            return cost
        except ValueError:
            self.logger.warning(f"Invalid cost format: {self.cost_input.text()}")
            return 0.0
        
    def has_valid_inputs(self) -> bool:
        try:
            price = self.get_sale_price()
            quantity = self.get_quantity()
            cost = self.get_cost_per_item()
            
            if not all([price > 0, quantity > 0, cost >= 0]):
                self.logger.debug(f"Invalid inputs: price={price}, quantity={quantity}, cost={cost}")
                return False
                
            self.logger.debug(f"Valid inputs: price={price}, quantity={quantity}, cost={cost}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating product inputs: {str(e)}", exc_info=True)
            return False