# BudgetFlow
## Overview

BudgetFlow is a personal budgeting application designed to help users manage and track their finances efficiently. Developed using Python, this application offers a user-friendly interface for creating profiles, tracking income and expenses, categorizing transactions, and visualizing spending habits through graphs and charts.


## Features
- **Secure User Authentication**: Multi-layered password protection with salted hashing
- **Comprehensive Transaction Management**: Record, categorize, filter, and analyze all financial activities
- **Smart Categorization**: Pre-defined and custom categories with color coding and icons for visual organization
- **Advanced Financial Analytics**: Detailed insights through interactive charts and customizable reports
- **Goal-Based Savings**: Set, track, and visualize progress toward financial goals
- **Data Visualization**: Interactive charts and graphs powered by Matplotlib
- **Privacy-Focused**: All data stored locally with no external connections
- **Cross-Platform Compatibility**: Works on Windows, macOS, and Linux


## Installation
### Prerequisites

- Python 3.8+
- Git (for cloning the repository)
- Tkinter support (included with most Python installations)

### Steps

1. Clone the repository:
   ```bash
     git clone https://github.com/yourusername/BudgetFlow.git
     cd BudgetFlow
   ```

2. Create a virtual environment (recommended):
   ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
     pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
     python setup_db.py
   ```

5. Run the application:
   ```bash
     python src/main.py
   ```


## Project Structure

BudgetFlow/
├── src/                    # Source code
│   ├── controllers/        # Application logic
│   ├── core/               # Core business logic
│   ├── models/             # Data models
│   ├── ui/                 # User interface components
│   └── utils/              # Utility functions
├── tests/                  # Test suite
├── data/                   # Database storage
└── docs/                   # Documentation


## Technologies Used

- **Backend**: Python 3.8+
- **Database**: SQLite3 with optimized query structure
- **GUI Framework**: Tkinter with custom styling
- **Data Visualization**: Matplotlib/Seaborn
- **Testing**: Pytest and Unittest frameworks
- **Version Control**: Git
- **Architecture**: MVC (Model-View-Controller) pattern


## Development Timeline

- Week 1 (Mar 20): Planning and Design
- Week 2 (Mar 27): User Authentication System
- Week 3 (Apr 3): Transaction Management
- Week 4 (Apr 10): Transaction UI & Reporting
- Week 5 (Apr 17): Savings Report Management
- Week 6 (Apr 24): Data Persistence & Full Reporting
- Week 7 (May 1): Testing & Documentation, Final Submission


## Usage
### First-time Setup
1. Launch the application
2. Create a new user account using the registration form
3. Log in with your credentials
4. Start by setting up your budget categories or use our pre-defined ones

### Adding Transactions
1. Navigate to the Transactions tab
2. Enter transaction details and select a category
3. Save the transaction to update your reports

### Viewing Reports
1. Navigate to the Reports tab
2. Select the date range and categories to analyze
3. View your spending patterns and saving progress


## Contributing
We welcome contributions to BudgetFlow! Please follow these steps:
1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request
Please make sure to update tests as appropriate.


## Development Team
- May Sabai
- Samriddhi Matharu


## Future Roadmap
- Budget alerts and notification system
- Mobile application development (iOS/Android)
- Cloud synchronization for multi-device access
- Financial insights with machine learning predictions
- Future: Multi-currency support with real-time exchange rates