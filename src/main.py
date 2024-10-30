# src/main.py
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)  # Changed from append to insert(0) to give it priority

from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow  # Changed to absolute import
from src.utils.config_loader import ConfigLoader

def main():
    # Add the project root directory to Python path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(project_root)
    
    # Load marketplace configurations
    marketplaces = {}
    marketplace_dir = os.path.join(project_root, "data", "marketplaces")
    for filename in os.listdir(marketplace_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(marketplace_dir, filename)
            marketplace = ConfigLoader.load_marketplace(filepath)
            marketplaces[marketplace.name] = marketplace
    
    # Load shipping configurations
    shipping_carriers = {}
    shipping_dir = os.path.join(project_root, "data", "shipping")
    for filename in os.listdir(shipping_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(shipping_dir, filename)
            carrier = ConfigLoader.load_shipping(filepath)
            shipping_carriers[carrier.name] = carrier
    
    # Create and show the application
    app = QApplication(sys.argv)
    window = MainWindow(marketplaces, shipping_carriers)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()