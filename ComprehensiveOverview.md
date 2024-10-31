# Marketplace Profit Calculator
## Comprehensive Technical Overview

## Project Status
This application is currently in development. It provides a PyQt5-based GUI for calculating selling profits across different marketplaces, taking into account various fees, shipping costs, and seller tiers. While the core functionality is implemented, several features are still pending implementation.

## System Architecture

### Core Models (`src/models/`)

#### `fee.py` - Fee Calculation Models
Handles the definition and calculation of different fee types.

**Classes:**
- `FeeType (Enum)`: Defines fee types (PERCENTAGE, FLAT, COMPOUND)
- `FeeApplication (Enum)`: Specifies fee application scope (PER_ITEM, PER_ORDER)
- `Fee (dataclass)`: 
  - Manages fee calculations with validation
  - Methods:
    - `_validate()`: Ensures fee has required values based on type
    - `calculate(base_amount, quantity)`: Computes fee amount based on type and application

#### `marketplace.py` - Marketplace Structure Models
Defines the structure of marketplaces and seller tiers.

**Classes:**
- `SellerTier (dataclass)`: 
  - Holds seller tier information and associated fees
  - Attributes: name, fees dictionary
- `Marketplace (dataclass)`: 
  - Contains marketplace configuration
  - Attributes: name, tiers dictionary

#### `shipping.py` - Shipping Models
Manages shipping rates and carrier information.

**Classes:**
- `ShippingRate (dataclass)`: 
  - Defines weight-based shipping rates
  - Attributes: weight_up_to, price
- `ShippingService (dataclass)`: 
  - Contains shipping service configuration
  - Attributes: name, weight_limits, manual_entry (optional)
  - Methods:
    - `get_rate(weight)`: Returns applicable rate for given weight
    - Supports both weight-based and manual price entry shipping methods
- `ShippingCarrier (dataclass)`: 
  - Holds carrier information and available services
  - Attributes: name, services dictionary
  - Supports both standard carriers and manual rate entry

### UI Components (`src/ui/`)

#### `main_window.py` - Main Application Window
Integrates all UI components and manages the main application flow.

**Class: MainWindow**
- Methods:
  - `setup_ui()`: Initializes and arranges UI components
  - `on_input_changed()`: Handles input change events
  - `calculate_profit()`: Triggers profit calculation and updates display
  - Handles both weight-based and manual shipping price calculations

#### `marketplace_widget.py` - Marketplace Selection UI
Handles marketplace and seller tier selection.

**Class: MarketplaceWidget**
- Methods:
  - `setup_ui()`: Creates marketplace selection interface
  - `update_seller_tiers()`: Updates available seller tiers
  - `get_selected_marketplace()`: Returns selected marketplace
  - `get_selected_tier()`: Returns selected seller tier

#### `product_widget.py` - Product Details UI
Manages product information input.

**Class: ProductWidget**
- Methods:
  - `setup_ui()`: Creates product input interface
  - `get_sale_price()`: Returns entered sale price
  - `get_quantity()`: Returns entered quantity
  - `get_cost_per_item()`: Returns entered cost per item
  - `has_valid_inputs()`: Validates all product inputs

#### `shipping_widget.py` - Shipping Options UI
Handles shipping carrier and service selection.

**Class: ShippingWidget**
- Methods:
  - `setup_ui()`: Creates shipping selection interface
  - `update_services()`: Updates available shipping services
  - `get_selected_carrier()`: Returns selected carrier
  - `get_selected_service()`: Returns selected service
  - `get_weight()`: Returns entered weight
  - `get_manual_price()`: Returns manually entered shipping price
  - `update_manual_price_visibility()`: Toggles visibility of manual price input
  - `has_valid_inputs()`: Validates all shipping inputs based on service type

#### `results_widget.py` - Results Display UI
Shows calculation results and fee breakdowns.

**Class: ResultsWidget**
- Methods:
  - `setup_ui()`: Creates results display interface
  - `update_results()`: Updates displayed calculation results
  - `reset_results()`: Resets display to default values

### Utilities (`src/utils/`)

#### `calculator.py` - Profit Calculation Logic
Handles core profit calculation functionality.

**Classes:**
- `ProfitCalculationResult (dataclass)`: Holds calculation results
- `ProfitCalculator`:
  - Methods:
    - `calculate_profit()`: Performs comprehensive profit calculation
    - Supports both weight-based and manual shipping price calculations
    - Validates inputs based on shipping service type

### Utilities (`src/utils/`)

#### `calculator.py` - Profit Calculation Logic
Handles core profit calculation functionality.

**Classes:**
- `ProfitCalculationResult (dataclass)`: Holds calculation results
- `ProfitCalculator`:
  - Methods:
    - `calculate_profit()`: Performs comprehensive profit calculation

#### `config_loader.py` - Configuration File Handler
Manages loading and parsing of JSON configuration files.

**Class: ConfigLoader**
- Static Methods:
  - `load_marketplace()`: Loads marketplace configuration from JSON
  - `load_shipping()`: Loads shipping configuration from JSON

#### `logger.py` - Logging Utility
Provides application-wide logging functionality.

**Class: Logger**
- Static Methods:
  - `setup()`: Initializes logging system
  - `get_logger()`: Returns logger instance
  - `shutdown()`: Cleans up logging resources
  - `flush()`: Ensures all logs are written

### Entry Point

#### `main.py` - Application Entry Point
Initializes and launches the application.

**Functions:**
- `main()`: 
  - Loads configurations
  - Creates main window
  - Starts application event loop

## Configuration Files

### Marketplace Configurations (`data/marketplaces/`)
- JSON files defining marketplace fee structures
- Currently includes:
  - TCGPlayer configuration with multiple seller tiers
  - Ebay example placeholder configuration
  - Whatnot example placeholder configuration

### Shipping Configurations (`data/shipping/`)
- JSON files defining shipping carrier services and rates
- Currently includes:
  - USPS configuration with First Class Package service
  - Manual shipping rate configuration for custom pricing
  - Fedex example placeholder configuration
  - UPS example placeholder configuration

## Implementation Status

✅ Implemented:
- Core data models and validation
- Fee calculation logic
- Basic GUI components
- Configuration loading
- Logging system
- Manual shipping price entry
- Dynamic shipping input validation

⏳ Pending:
- Comprehensive test suite
- Error handling dialogs
- Input validation improvements
- Save/Load functionality
- Tax calculations
- Bulk calculation features
- Data export functionality