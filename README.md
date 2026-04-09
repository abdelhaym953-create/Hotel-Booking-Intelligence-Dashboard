# Hotel Booking Analytics Dashboard

## Overview
This project provides a comprehensive analysis of hotel booking data, including data cleaning, exploratory data analysis, and an interactive dashboard for business insights. The dashboard helps hotel managers understand booking patterns, cancellation rates, customer behavior, and revenue trends.

## Features

### Data Cleaning and Preparation
- Load and clean hotel booking data from CSV
- Handle missing values, duplicates, and data inconsistencies
- Create derived features like total stay duration, total guests, and revenue
- Filter invalid bookings (e.g., zero guests, negative ADR)

### Interactive Dashboard
- **Overview Page**: Key performance indicators (KPIs), monthly booking trends, hotel type distribution, top countries, customer types, and revenue trends
- **Analysis Page**: Business insights including demand analysis, cancellation causes, and customer segmentation

### Visualizations
- Bar charts for monthly bookings and top countries
- Pie chart for hotel type distribution
- Line charts for revenue trends and demand patterns
- Interactive plots using Plotly Express

## Technologies Used
- **Python**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Plotly Express**: Data visualization
- **Streamlit**: Web application framework for the dashboard

## Project Structure
```
.
├── hotel_booking.ipynb          # Jupyter notebook for data cleaning and analysis
├── hotel_booking.csv            # Raw hotel booking data
├── hotel_booking_cleaned.csv    # Cleaned dataset
├── Overview.py                  # Main Streamlit dashboard page
├── pages/
│   └── analysis.py              # Business insights page
└── README.md                    # Project documentation
```

## Installation and Setup

1. **Clone or download the project files**

2. **Install required packages**:
   ```bash
   pip install pandas numpy plotly streamlit
   ```

3. **Ensure data files are present**:
   - `hotel_booking.csv` (raw data)
   - `hotel_booking_cleaned.csv` (processed data)

## Usage

### Running the Dashboard
1. Open a terminal in the project directory
2. Run the Streamlit app:
   ```bash
   streamlit run Overview.py
   ```
3. Open your web browser to the provided URL (usually http://localhost:8501)

### Data Analysis
- Open `hotel_booking.ipynb` in Jupyter Notebook or JupyterLab to explore the data cleaning process
- The notebook contains step-by-step data preprocessing and feature engineering

## Data Source
The analysis is based on hotel booking data containing information about:
- Hotel types (City Hotel, Resort Hotel)
- Booking details (arrival dates, length of stay, guests)
- Customer information (country, customer type, deposit type)
- Cancellation status and pricing (ADR - Average Daily Rate)

## Key Insights
- **Demand Patterns**: Seasonal variations in booking volumes
- **Cancellation Factors**: Impact of deposit types on cancellation rates
- **Customer Segments**: Distribution of customer types and their booking behavior
- **Revenue Trends**: Year-over-year revenue performance

## Contributing
Feel free to contribute by:
- Adding new visualizations
- Implementing additional analysis features
- Improving the dashboard UI/UX
- Enhancing data cleaning processes

## License
This project is for educational and analytical purposes.