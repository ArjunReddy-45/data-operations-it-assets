# IT Asset Data Operations & Insights

A comprehensive mini-project demonstrating end-to-end data engineering workflows with real-world IT asset data, from Excel cleaning to Elasticsearch indexing and business intelligence insights.

## 🎯 Project Overview

This project simulates real-world enterprise data challenges by working with a "messy" IT asset inventory dataset. The workflow includes data cleaning, indexing into Elasticsearch, data transformation, and building meaningful business insights through visualizations.

## 📁 Project Structure

```
data-operations-it-assets/
├── it_asset_inventory_cleaned.csv    # Cleaned dataset from Phase 1
├── index_data.py                     # Phase 2: Data indexing script
├── transform_data.py                 # Phase 3: Data transformation script
├── visualization_screenshots/        # Phase 4: Dashboard screenshots
├── README.md                        # This file
└── final_report.md                  # Comprehensive project report
```

## 🚀 Phases Completed

### Phase 1: Excel Data Cleaning ✅

**Objective**: Clean the raw dataset and prepare it for Elasticsearch ingestion.

**Excel Functions Used**:
- `Remove Duplicates` feature to eliminate duplicate hostnames
- `=TRIM()` function to remove extra spaces from text fields
- Find & Replace to handle missing values (replaced blanks with "Unknown")
- Date formatting to ensure consistent YYYY-MM-DD format
- Data validation to check for consistency

**Data Quality Improvements**:
- Removed duplicate records based on hostname field
- Standardized text formatting by trimming whitespace
- Handled missing values consistently
- Validated and corrected date formats
- Final clean dataset: `it_asset_inventory_cleaned.csv`

### Phase 2: Elasticsearch Indexing ✅

**Objective**: Load cleaned CSV data into Elasticsearch using Python.

**Key Features of `index_data.py`**:
- Robust connection handling with Elasticsearch Cloud
- Data validation and cleaning (handles null values, duplicates)
- Proper index mapping for optimal search performance
- Bulk upload with detailed error handling
- Document verification and statistics

**Technical Implementation**:
```python
# Key components:
- Elasticsearch connection with API key authentication
- Pandas for CSV data processing
- Data cleaning (null handling, duplicate resolution)
- Index mapping definition for proper field types
- Bulk indexing with error reporting
- Post-indexing verification
```

### Phase 3: Data Transformation & Enrichment ✅

**Objective**: Enhance indexed data with derived fields and business logic.

**Key Features of `transform_data.py`**:
- **Risk Assessment**: Automatically categorizes assets as High/Medium/Low risk based on lifecycle status
- **System Age Calculation**: Computes age in years from installation date
- **Age Categorization**: Groups systems as New (<2 years), Mature (2-5 years), or Legacy (>5 years)
- **Compliance Status**: Determines compliance based on risk level and age
- **Data Quality**: Filters out records with missing critical information

**Transformations Applied**:
1. **Risk Level Derivation**:
   - High: EOL/EOS systems
   - Medium: Deprecated/Unsupported systems
   - Low: Supported systems

2. **System Age Analysis**:
   - Calculated from installation date to current date
   - Categorized for easier business analysis

3. **Compliance Assessment**:
   - Non-Compliant: High risk or Legacy systems
   - At-Risk: Medium risk systems
   - Compliant: Low risk, newer systems

## 🔧 Setup Instructions

### Prerequisites
```bash
pip install elasticsearch pandas
```

### Environment Setup
1. Clone this repository
2. Update Elasticsearch credentials in both Python scripts
3. Ensure CSV file path is correct in `index_data.py`

### Running the Scripts

1. **Index Original Data**:
   ```bash
   python index_data.py
   ```

2. **Transform and Enrich Data**:
   ```bash
   python transform_data.py
   ```

## 📊 Expected Outcomes

By completing this project, you will have:

✅ **Data Engineering Skills**:
- Excel data cleaning techniques
- Python scripting for data processing
- Elasticsearch indexing and transformations

✅ **Technical Implementation**:
- Robust error handling and data validation
- Scalable bulk data processing
- Advanced Elasticsearch scripting with Painless

✅ **Business Intelligence**:
- Risk assessment automation
- Compliance monitoring capabilities
- Asset lifecycle management insights

## 🔍 Key Metrics & Insights

*Note: Actual insights will be populated after running the scripts and analyzing the data*

- Total assets processed: [To be updated]
- Risk distribution: [To be updated]
- Compliance status: [To be updated]
- Age distribution: [To be updated]

## 🛠️ Technical Stack

- **Data Processing**: Python, Pandas
- **Search & Analytics**: Elasticsearch
- **Data Cleaning**: Microsoft Excel
- **Version Control**: Git, GitHub
- **Visualization**: Kibana (Phase 4)

## 📈 Next Steps

- [ ] Phase 4: Create Kibana visualizations and dashboards
- [ ] Phase 5: Complete final report with business insights
- [ ] Export dashboard screenshots
- [ ] Document business recommendations

## 🤝 Contributing

This is an educational project. Feel free to fork and experiment with different data transformation techniques or visualization approaches.

## 📝 License

This project is for educational purposes. Dataset is simulated for learning data engineering concepts.
Mini Project: IT Asset Data Operations &amp; Insights
