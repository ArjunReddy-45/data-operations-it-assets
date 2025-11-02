# IT Asset Data Operations & Insights# IT Asset Data Operations & Insights



A comprehensive data engineering project for IT infrastructure asset management, risk assessment, and business intelligence.A comprehensive mini-project demonstrating end-to-end data engineering workflows with real-world IT asset data, from Excel cleaning to Elasticsearch indexing and business intelligence insights.



## 🎯 Project Overview## Project Overview



This project demonstrates end-to-end data operations for IT asset management, from Excel data cleaning through Elasticsearch indexing to Kibana visualization dashboards. The solution provides executive-level insights for infrastructure security, compliance, and strategic planning.This project simulates real-world enterprise data challenges by working with a "messy" IT asset inventory dataset. The workflow includes data cleaning, indexing into Elasticsearch, data transformation, and building meaningful business insights through visualizations.



## 📊 Key Results## Project Structure



- **327 IT assets** analyzed across global locations```

- **Risk assessment** based on OS lifecycle status (EOL/EOS detection)data-operations-it-assets/

- **Geographic distribution** analysis for compliance planning├── it_asset_inventory_cleaned.csv    # Cleaned dataset from Phase 1

- **Interactive dashboards** for executive decision-making├── index_data.py                     # Phase 2: Data indexing script

- **Vendor risk analysis** across major OS providers├── transform_data.py                 # Phase 3: Data transformation script

├── visualization_screenshots/        # Phase 4: Dashboard screenshots

## 🏗️ Architecture├── README.md                        # This file

└── final_report.md                  # Comprehensive project report

``````

Excel Data → Python Processing → Elasticsearch Cloud → Kibana Dashboards

```## Phases Completed



## 📁 Project Structure### Phase 1: Excel Data Cleaning



```**Objective**: Clean the raw dataset and prepare it for Elasticsearch ingestion.

data-operations-it-assets/

├── it_asset_inventory_cleaned.csv  # Cleaned dataset (327 records)**Excel Functions Used**:

├── index_data.py                   # Elasticsearch data ingestion- `Remove Duplicates` feature to eliminate duplicate hostnames

├── transform_data.py               # Risk assessment & data enrichment- `=TRIM()` function to remove extra spaces from text fields

├── visualization_screenshots/       # Dashboard screenshots- Find & Replace to handle missing values (replaced blanks with "Unknown")

├── README.md                       # Project documentation- '=UPPER()' is used to convert text into upper case

└── final_report.md                # Executive summary & insights- Date formatting to ensure consistent YYYY-MM-DD format

```- Data validation to check for consistency



## 🚀 Quick Start**Data Quality Improvements**:

- Removed duplicate records based on hostname field

### Prerequisites- Standardized text formatting by trimming whitespace

- Python 3.8+- Handled missing values consistently

- Elasticsearch Cloud account- '=UPPER()' is used to convert text into upper case

- Required packages: `elasticsearch`, `pandas`- Validated and corrected date formats

- Final clean dataset: `it_asset_inventory_cleaned.csv`

### Setup

1. **Clone the repository**### Phase 2: Elasticsearch Indexing 

   ```bash

   git clone https://github.com/ArjunReddy-45/data-operations-it-assets.git**Objective**: Load cleaned CSV data into Elasticsearch using Python.

   cd data-operations-it-assets

   ```**Key Features of `index_data.py`**:

- Robust connection handling with Elasticsearch Cloud

2. **Install dependencies**- Data validation and cleaning (handles null values, duplicates)

   ```bash- Proper index mapping for optimal search performance

   pip install elasticsearch pandas- Bulk upload with detailed error handling

   ```- Document verification and statistics



3. **Configure Elasticsearch****Technical Implementation**:

   - Update API keys in `index_data.py` and `transform_data.py````python

   - Set your Elasticsearch Cloud endpoint# Key components:

- Elasticsearch connection with API key authentication

4. **Run the pipeline**- Pandas for CSV data processing

   ```bash- Data cleaning (null handling, duplicate resolution)

   python index_data.py      # Index clean data- Index mapping definition for proper field types

   python transform_data.py  # Apply transformations- Bulk indexing with error reporting

   ```- Post-indexing verification

```

## 📈 Business Value

### Phase 3: Data Transformation & Enrichment 

### Risk Management

- **High-risk asset identification** (EOL/EOS systems)**Objective**: Enhance indexed data with derived fields and business logic.

- **Geographic risk distribution** for compliance planning

- **Internet exposure analysis** for security prioritization**Key Features of `transform_data.py`**:

- **Risk Assessment**: Automatically categorizes assets as High/Medium/Low risk based on lifecycle status

### Strategic Planning- **System Age Calculation**: Computes age in years from installation date

- **Vendor consolidation opportunities** - **Age Categorization**: Groups systems as New (<2 years), Mature (2-5 years), or Legacy (>5 years)

- **Infrastructure modernization roadmap**- **Compliance Status**: Determines compliance based on risk level and age

- **Compliance requirement mapping**- **Data Quality**: Filters out records with missing critical information



### Cost Optimization**Transformations Applied**:

- **License management insights**1. **Risk Level Derivation**:

- **Regional resource allocation**   - High: EOL/EOS systems

- **Security investment prioritization**   - Low: Supported systems



## 🎨 Visualizations2. **System Age Analysis**:

   - Calculated from installation date to current date

The project includes 4 executive dashboards:   - Categorized for easier business analysis



1. **Global Asset Distribution** - Geographic spread analysis3. **Compliance Assessment**:

2. **OS Risk Assessment Matrix** - Security risk by operating system   - Non-Compliant: High risk or Legacy systems

3. **Vendor Risk Distribution** - Provider-specific risk profiles   - Compliant: Low risk, newer systems

4. **Executive Overview Dashboard** - Combined strategic insights

## Setup Instructions

See `visualization_screenshots/` for dashboard examples.

### Prerequisites

## 🔧 Technical Features```bash

pip install elasticsearch pandas

- **Data Quality**: Automated cleaning and validation```

- **Risk Assessment**: EOL/EOS lifecycle status detection

- **Geographic Analysis**: Country-wise asset distribution### Environment Setup

- **Scalable Architecture**: Cloud-native Elasticsearch integration1. Clone this repository

- **Interactive Analytics**: Real-time Kibana dashboards2. Update Elasticsearch credentials in both Python scripts

3. Ensure CSV file path is correct in `index_data.py`

## 📊 Key Metrics

### Running the Scripts

- **Data Volume**: 327 IT assets processed

- **Geographic Coverage**: 8+ countries analyzed1. **Index Original Data**:

- **Risk Categories**: High/Low risk classification   ```bash

- **Vendor Analysis**: 8+ major OS providers assessed   python index_data.py

- **Data Quality**: 100% hostname validation   ```



## 🏆 Project Outcomes2. **Transform and Enrich Data**:

   ```bash

✅ **Complete data pipeline** from Excel to interactive dashboards     python transform_data.py

✅ **Executive-ready visualizations** for strategic decision-making     ```

✅ **Risk-based prioritization** for security and compliance  

✅ **Geographic insights** for regional planning  ## Expected Outcomes

✅ **Vendor analysis** for strategic partnerships  

By completing this project, you will have:

## 📝 License

**Data Engineering Skills**:

This project is for educational and demonstration purposes.- Excel data cleaning techniques

- Python scripting for data processing

## 👨‍💻 Author- Elasticsearch indexing and transformations



**Arjun Reddy Tadi**  **Technical Implementation**:

Data Engineering & Analytics Project  - Robust error handling and data validation

GitHub: [@ArjunReddy-45](https://github.com/ArjunReddy-45)- Scalable bulk data processing
- Advanced Elasticsearch scripting with Painless

**Business Intelligence**:
- Risk assessment automation
- Compliance monitoring capabilities
- Asset lifecycle management insights

## Key Metrics & Insights

**Final Project Results**:

- **Total assets processed**: 327 clean records (from 328 original, 1 unknown hostname removed)
- **Risk distribution**: High/Low risk classification based on EOL/EOS status
- **Geographic spread**: 8+ countries with UNKNOWN, Brazil, USA as top locations
- **OS diversity**: Multiple operating systems requiring standardization
- **Business criticality**: Internet-facing assets with enhanced risk scoring

**Critical Business Findings**:
- 16.82% Unknown locations requiring urgent classification
- Mixed risk distribution across geographic regions
- Internet exposure correlation with security risks
- Vendor consolidation opportunities identified

## Technical Stack

- **Data Processing**: Python, Pandas
- **Search & Analytics**: Elasticsearch
- **Data Cleaning**: Microsoft Excel
- **Version Control**: Git, GitHub
- **Visualization**: Kibana (Phase 4)

### Phase 4: Kibana Visualizations & Dashboards

**Objective**: Create executive-level dashboards for business intelligence and decision-making.

**Visualizations Created**:
1. **Assets by Country (Pie Chart)**: Geographic distribution showing UNKNOWN (16.82%), Brazil (13.46%), USA (11.93%)
2. **OS Risk Analysis (Horizontal Bar)**: Risk levels by operating system with Unknown systems leading (~50 assets)
3. **OS Security Profile (Sunburst Chart)**: Detailed risk breakdown with 19.27% Unknown systems in high-risk category
4. **Vendor Risk Distribution (Stacked Bar)**: Strategic vendor risk analysis across major OS providers

**Executive Dashboard**: Combined all visualizations into comprehensive "IT Asset Risk Dashboard" for strategic decision-making.

**Business Value**:
- Geographic risk hotspot identification
- Security prioritization by OS platform
- Vendor management strategy support
- Compliance planning for regional requirements

### Phase 5: Final Documentation & GitHub Commit 

**Objective**: Complete project documentation and repository finalization.

**Deliverables**:
- Comprehensive README with full project documentation
- Project summary report with business insights
- Complete file structure documentation
- Dashboard screenshots and results
- Technical implementation details

