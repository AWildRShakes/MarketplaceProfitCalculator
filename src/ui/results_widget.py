# src/ui/results_widget.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                            QGridLayout, QGroupBox)
from ..models.marketplace import Marketplace

class ResultsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Results Group
        results_group = QGroupBox("Calculation Results")
        results_layout = QGridLayout()
        
        # Create labels for all results
        self.gross_revenue_label = QLabel("Gross Revenue: $0.00")
        self.marketplace_fees_label = QLabel("Total Marketplace Fees: $0.00")
        self.shipping_cost_label = QLabel("Shipping Cost: $0.00")
        self.total_cost_label = QLabel("Total Cost: $0.00")
        self.net_profit_label = QLabel("Net Profit: $0.00")
        self.profit_margin_label = QLabel("Profit Margin: 0.00%")
        
        # Add labels to layout
        results_layout.addWidget(self.gross_revenue_label, 0, 0)
        results_layout.addWidget(self.marketplace_fees_label, 1, 0)
        results_layout.addWidget(self.shipping_cost_label, 2, 0)
        results_layout.addWidget(self.total_cost_label, 3, 0)
        results_layout.addWidget(self.net_profit_label, 4, 0)
        results_layout.addWidget(self.profit_margin_label, 5, 0)
        
        # Fee breakdown section
        self.fee_breakdown_group = QGroupBox("Fee Breakdown")
        self.fee_breakdown_layout = QVBoxLayout()
        self.fee_breakdown_group.setLayout(self.fee_breakdown_layout)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        layout.addWidget(self.fee_breakdown_group)
    
    def update_results(self, calculation_result):
        self.gross_revenue_label.setText(f"Gross Revenue: ${calculation_result.gross_revenue:.2f}")
        self.marketplace_fees_label.setText(f"Total Marketplace Fees: ${calculation_result.total_marketplace_fees:.2f}")
        self.shipping_cost_label.setText(f"Shipping Cost: ${calculation_result.shipping_cost:.2f}")
        self.total_cost_label.setText(f"Total Cost: ${calculation_result.total_cost:.2f}")
        self.net_profit_label.setText(f"Net Profit: ${calculation_result.net_profit:.2f}")
        self.profit_margin_label.setText(f"Profit Margin: {calculation_result.profit_margin:.2f}%")
        
        # Update fee breakdown
        # Clear previous fee breakdown
        for i in reversed(range(self.fee_breakdown_layout.count())): 
            self.fee_breakdown_layout.itemAt(i).widget().setParent(None)
        
        # Add new fee breakdown
        for fee_name, fee_amount in calculation_result.fee_breakdown.items():
            self.fee_breakdown_layout.addWidget(
                QLabel(f"{fee_name}: ${fee_amount:.2f}")
            )