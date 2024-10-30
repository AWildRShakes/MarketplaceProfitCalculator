from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QLineEdit, QGridLayout, QGroupBox)
from PyQt5.QtCore import pyqtSignal
from src.models.shipping import ShippingCarrier
from src.utils.logger import Logger

class ShippingWidget(QWidget):
    input_changed = pyqtSignal()
    
    def __init__(self, carriers: dict[str, ShippingCarrier], parent=None):
        super().__init__(parent)
        self.carriers = carriers
        self.logger = Logger.get_logger()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Shipping Group
        shipping_group = QGroupBox("Shipping Settings")
        shipping_layout = QGridLayout()
        
        # Carrier selection
        shipping_layout.addWidget(QLabel("Carrier:"), 0, 0)
        self.carrier_combo = QComboBox()
        self.carrier_combo.addItems(self.carriers.keys())
        self.carrier_combo.currentTextChanged.connect(self.update_services)
        self.carrier_combo.currentTextChanged.connect(self.input_changed.emit)
        shipping_layout.addWidget(self.carrier_combo, 0, 1)
        
        # Service selection
        shipping_layout.addWidget(QLabel("Service:"), 1, 0)
        self.service_combo = QComboBox()
        self.service_combo.currentTextChanged.connect(self.input_changed.emit)
        shipping_layout.addWidget(self.service_combo, 1, 1)
        
        # Weight input
        shipping_layout.addWidget(QLabel("Weight per item (oz):"), 2, 0)
        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Enter weight")
        self.weight_input.textChanged.connect(self.input_changed.emit)
        shipping_layout.addWidget(self.weight_input, 2, 1)
        
        shipping_group.setLayout(shipping_layout)
        layout.addWidget(shipping_group)
        
        # Initialize services
        self.update_services()
        self.logger.debug("ShippingWidget UI setup completed")
    
    def update_services(self):
        carrier_name = self.carrier_combo.currentText()
        self.service_combo.clear()
        if carrier_name in self.carriers:
            self.service_combo.addItems(self.carriers[carrier_name].services.keys())
            self.logger.debug(f"Updated services for carrier: {carrier_name}")
        else:
            self.logger.warning(f"Invalid carrier selected: {carrier_name}")
    
    def get_selected_carrier(self) -> str:
        carrier = self.carrier_combo.currentText()
        if not carrier:
            self.logger.warning("No carrier selected")
        return carrier
    
    def get_selected_service(self) -> str:
        service = self.service_combo.currentText()
        if not service:
            self.logger.warning("No shipping service selected")
        return service
    
    def get_weight(self) -> float:
        try:
            weight = float(self.weight_input.text())
            if weight <= 0:
                self.logger.warning(f"Invalid weight entered: {weight}")
                return 0.0
            return weight
        except ValueError:
            self.logger.warning(f"Invalid weight format: {self.weight_input.text()}")
            return 0.0
    
    def has_valid_inputs(self) -> bool:
        try:
            # Check if carrier is selected
            carrier_name = self.get_selected_carrier()
            if not carrier_name or carrier_name not in self.carriers:
                self.logger.debug("Invalid or missing carrier selection")
                return False
            
            # Check if service is selected
            service_name = self.get_selected_service()
            if not service_name or service_name not in self.carriers[carrier_name].services:
                self.logger.debug("Invalid or missing service selection")
                return False
            
            # Check if weight is valid
            weight = self.get_weight()
            if weight <= 0:
                self.logger.debug(f"Invalid weight: {weight}")
                return False
            
            # Check if weight is within service limits
            service = self.carriers[carrier_name].services[service_name]
            if (weight < service.weight_limits['min'] or 
                weight > service.weight_limits['max']):
                self.logger.debug(f"Weight {weight} outside service limits: "
                                f"min={service.weight_limits['min']}, "
                                f"max={service.weight_limits['max']}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating shipping inputs: {str(e)}", exc_info=True)
            return False