# Marketplace App
## This app is currently in development and should not be used for calculations yet.
A PyQt5-based GUI application for calculating selling profits across different marketplaces, taking into account various fees, shipping costs, and seller tiers.

## Project Structure

```
├── MarketplaceApp/
    ├── data/
    │   ├── marketplaces/
    │   │   ├── ebay.json
    │   │   ├── tcgplayer.json
    │   │   └── whatnot.json
    │   └── shipping/
    │       ├── fedex.json
    │       ├── ups.json
    │       └── usps.json
    ├── logs/
    ├── src/
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── fee.py
    │   │   ├── marketplace.py
    │   │   └── shipping.py
    │   ├── ui/
    │   │   ├── __init__.py
    │   │   ├── main_window.py
    │   │   ├── marketplace_widget.py
    │   │   ├── product_widget.py
    │   │   ├── results_widget.py
    │   │   └── shipping_widget.py
    │   ├── utils/
    │   │   ├── __init__.py
    │   │   ├── calculator.py
    │   │   ├── config_loader.py
    │   │   └── logger.py
    │   ├── __init__.py
    │   └── main.py
    ├── tests/
    │   ├── __init__.py
    │   ├── test_calculator.py
    │   ├── test_marketplace.py
    │   └── test_shipping.py
    ├── README.md
    └── requirements.txt
```

## Code Overview

### Models (`src/models/`)

- `fee.py`: Defines fee types (percentage, flat, compound) and calculation logic
  - `FeeType`: Enum for different fee types
  - `FeeApplication`: Enum for fee application (per item/order)
  - `Fee`: Dataclass for fee calculation

- `marketplace.py`: Marketplace and seller tier structures
  - `SellerTier`: Dataclass for seller tier information
  - `Marketplace`: Dataclass for marketplace configuration

- `shipping.py`: Shipping carrier and rate structures
  - `ShippingRate`: Dataclass for weight-based rates
  - `ShippingService`: Dataclass for shipping service options
  - `ShippingCarrier`: Dataclass for carrier information

### UI Components (`src/ui/`)

- `main_window.py`: Main application window integrating all components
- `marketplace_widget.py`: Marketplace and seller tier selection
- `product_widget.py`: Product details input (price, quantity, cost)
- `shipping_widget.py`: Shipping carrier and service selection
- `results_widget.py`: Displays calculation results and fee breakdown

### Utilities (`src/utils/`)

- `calculator.py`: Core profit calculation logic
  - `ProfitCalculator`: Handles all fee and profit calculations
  - `ProfitCalculationResult`: Dataclass for calculation results

- `config_loader.py`: JSON configuration file handling
  - `ConfigLoader`: Static methods for loading marketplace and shipping configs

## Configuration Files

### Marketplace Configuration (`data/marketplaces/`)

```json
{
    "name": "TCGPlayer",
    "tiers": {
        "marketplace_seller": {
            "name": "Marketplace Seller (Level 1-4 Account)",
            "fees": {
                "marketplace_commission": {
                    "type": "percentage",
                    "value": 10.25,
                    "application": "per_item"
                },
                "processing_fee": {
                    "type": "compound",
                    "percentage": 2.5,
                    "flat_fee": 0.30,
                    "application": "per_order"
                }
            }
        }
    }
}
```

### Shipping Configuration (`data/shipping/`)

```json
{
    "name": "USPS",
    "services": {
        "first_class": {
            "name": "First Class Package",
            "weight_limits": {
                "min": 0,
                "max": 16
            },
            "rates": [
                {
                    "weight_up_to": 4,
                    "price": 4.50
                },
                {
                    "weight_up_to": 8,
                    "price": 5.25
                }
            ]
        }
    }
}
```

## Setup and Running

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Create necessary JSON configuration files in `data/marketplaces/` and `data/shipping/`

3. Run the application:
```bash
python src/main.py
```

## Current Implementation Status

- ✅ Core data models
- ✅ Fee calculation logic
- ✅ GUI components
- ✅ Configuration loading
- ⏳ Test suite (to be implemented)
- ⏳ Error handling dialogs
- ⏳ Input validation
- ⏳ Save/Load functionality for frequent calculations

## Future Enhancements

1. Add comprehensive error handling and user feedback
2. Implement input validation
3. Add save/load functionality for calculations
4. Create test suite
5. Add support for tax calculations
6. Implement bulk calculation features
7. Add data export functionality