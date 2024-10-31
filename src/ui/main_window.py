from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                            QMessageBox)
from ui.marketplace_widget import MarketplaceWidget
from ui.shipping_widget import ShippingWidget
from ui.product_widget import ProductWidget
from ui.results_widget import ResultsWidget
from src.utils.calculator import ProfitCalculator
from src.utils.logger import Logger

class MainWindow(QMainWindow):
    def __init__(self, marketplaces, shipping_carriers):
        super().__init__()
        self.marketplaces = marketplaces
        self.shipping_carriers = shipping_carriers
        self.logger = Logger.get_logger()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Marketplace Profit Calculator")
        self.setMinimumWidth(800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create widgets
        self.product_widget = ProductWidget()
        self.marketplace_widget = MarketplaceWidget(self.marketplaces)
        self.shipping_widget = ShippingWidget(self.shipping_carriers)
        self.results_widget = ResultsWidget()
        
        # Create calculate button
        self.calculate_button = QPushButton("Calculate Profit")
        self.calculate_button.clicked.connect(self.calculate_profit)
        
        # Add widgets to layout
        layout.addWidget(self.product_widget)
        layout.addWidget(self.marketplace_widget)
        layout.addWidget(self.shipping_widget)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.results_widget)
        
        # Connect signals
        self.product_widget.input_changed.connect(self.on_input_changed)
        self.marketplace_widget.input_changed.connect(self.on_input_changed)
        self.shipping_widget.input_changed.connect(self.on_input_changed)
        
        self.logger.info("Main window UI setup completed")
    
    def on_input_changed(self):
        # Only calculate if we have all required inputs
        if (self.product_widget.has_valid_inputs() and 
            self.marketplace_widget.get_selected_marketplace() and
            self.shipping_widget.has_valid_inputs()):
            self.calculate_profit()
    
    def calculate_profit(self):
        try:
            # Get selected marketplace and carrier
            marketplace_name = self.marketplace_widget.get_selected_marketplace()
            carrier_name = self.shipping_widget.get_selected_carrier()
            
            self.logger.debug(f"Calculating profit for marketplace: {marketplace_name}, "
                            f"carrier: {carrier_name}")
            
            marketplace = self.marketplaces[marketplace_name]
            carrier = self.shipping_carriers[carrier_name]
            
            # Get shipping service and check if it's manual entry
            service_id = self.shipping_widget.get_selected_service()
            service = carrier.services[service_id]
            is_manual = getattr(service, 'manual_entry', False)
            
            # Prepare shipping parameters
            manual_shipping_price = None
            weight_per_item = 0.0
            
            if is_manual:
                manual_shipping_price = self.shipping_widget.get_manual_price()
                self.logger.debug(f"Using manual shipping price: ${manual_shipping_price:.2f}")
            else:
                weight_per_item = self.shipping_widget.get_weight()
                self.logger.debug(f"Using weight-based shipping: {weight_per_item}oz")
            
            # Create calculator
            calculator = ProfitCalculator(marketplace, carrier)
            
            # Calculate profit
            result = calculator.calculate_profit(
                sale_price=self.product_widget.get_sale_price(),
                quantity=self.product_widget.get_quantity(),
                cost_per_item=self.product_widget.get_cost_per_item(),
                weight_per_item=weight_per_item,
                tier_id=self.marketplace_widget.get_selected_tier(),
                shipping_service_id=service_id,
                manual_shipping_price=manual_shipping_price
            )
            
            # Update results
            self.results_widget.update_results(result)
            
        except ValueError as e:
            self.logger.warning(f"Validation error in calculation: {str(e)}")
            QMessageBox.warning(self, "Input Error", str(e))
        except Exception as e:
            self.logger.error(f"Error calculating profit: {str(e)}", exc_info=True)
            QMessageBox.critical(self, "Error", 
                               "An error occurred while calculating profit. Check the logs for details.")