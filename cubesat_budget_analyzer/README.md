# CubeSat Budget Analyzer

A comprehensive tool for analyzing link and data budgets for CubeSat missions. This application helps satellite engineers and researchers calculate and optimize their CubeSat's communication and data handling capabilities.

## Features

### Link Budget Analysis
- Transmitter parameters (power, gain, losses)
- Channel characteristics (frequency, distance, atmospheric loss)
- Receiver parameters (gain, losses, system temperature)
- Modulation and coding schemes
- Comprehensive link margin calculations

### Data Budget Analysis
- Storage capacity planning
- Multiple data source management
- Data generation rate analysis
- Transmission capacity calculations
- Storage buffer margin assessment

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Install from source
1. Clone the repository:
```bash
git clone https://github.com/yourusername/cubesat-budget-analyzer.git
cd cubesat-budget-analyzer
```

2. Install the package:
```bash
pip install -e .
```

## Usage

### Launch the application
```bash
cubesat-budget-analyzer
```

### Link Budget Analysis
1. Enter transmitter parameters:
   - Transmit power
   - Antenna gain
   - System losses

2. Specify channel characteristics:
   - Operating frequency
   - Link distance
   - Atmospheric losses

3. Input receiver parameters:
   - Antenna gain
   - System losses
   - System temperature

4. Select modulation and coding schemes

5. Click "Calculate Link Budget" to view results

### Data Budget Analysis
1. Configure storage parameters:
   - Total storage capacity
   - OS reserved space
   - Redundancy factor

2. Add data generation sources:
   - Source name
   - Data rate
   - Duty cycle
   - Compression ratio

3. Set transmission parameters:
   - Downlink data rate
   - Ground station access time
   - Protocol overhead

4. Click "Calculate Data Budget" to view results

## Project Structure
```
cubesat_budget_analyzer/
├── src/
│   └── cubesat_budget_analyzer/
│       ├── gui/
│       │   ├── tabs/
│       │   │   ├── link_budget_tab.py
│       │   │   └── data_budget_tab.py
│       │   └── main_window.py
│       └── __main__.py
├── setup.py
└── README.md
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details. 