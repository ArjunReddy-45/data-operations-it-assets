"""from elasticsearch import Elasticsearch, helpers

IT Asset Inventory - Elasticsearch Data Indexingimport pandas as pd

==============================================import os

from datetime import datetime

This script processes cleaned IT asset inventory data and indexes it into Elasticsearchimport json

for advanced analytics and visualization. It includes robust error handling, data validation,

and bulk upload capabilities for optimal performance.# Configuration

ES_ENDPOINT = "https://my-elasticsearch-project-e74838.es.asia-south1.gcp.elastic.cloud:443"

Dependencies:ES_API_KEY = "NXFiZUxwb0JOOUVTMksyeElqa0U6S051T2V2NnFJSlBaNW5ZOFZWaU5odw=="

- elasticsearch>=8.0.0CSV_FILE = "C:/Users/ArjunReddyTadi/Desktop/mylearning/it_asset_inventory_cleaned.csv"

- pandas>=1.3.0TARGET_INDEX = "it_assets_index"

- CSV file: it_asset_inventory_cleaned.csv# === CONNECT TO ELASTIC ===

es = Elasticsearch(

Author: IT Data Engineering Team    ES_ENDPOINT,

Date: November 2025    api_key=ES_API_KEY,

"""    verify_certs=False  # Temporary fix for SSL issues

)

import pandas as pd

from elasticsearch import Elasticsearch, helpers# === CHECK CONNECTION ===

import loggingif not es.ping():

from datetime import datetime    print("❌ Connection failed! Please check endpoint or API key.")

    exit()

# Configure logging for monitoring and debuggingelse:

logging.basicConfig(    print("✅ Connected to Elasticsearch!")

    level=logging.INFO,

    format='%(asctime)s - %(levelname)s - %(message)s',# === READ CSV FILE ===

    handlers=[if not os.path.exists(CSV_FILE):

        logging.FileHandler('indexing.log'),    print(f"❌ CSV file not found: {CSV_FILE}")

        logging.StreamHandler()    exit()

    ]

)df = pd.read_csv(CSV_FILE)

logger = logging.getLogger(__name__)print(f"📄 Loaded {len(df)} records from {CSV_FILE}")



class ITAssetIndexer:# === DATA VALIDATION AND CLEANING ===

    """print("🧹 Validating and cleaning data...")

    Handles indexing of IT asset inventory data into Elasticsearch.

    """# Remove rows with empty hostnames

    initial_count = len(df)

    def __init__(self, cloud_id, api_key):df = df.dropna(subset=['hostname'])

        """df = df[df['hostname'].str.strip() != '']

        Initialize Elasticsearch connection.

        # Remove unnamed columns if they exist

        Args:df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            cloud_id (str): Elasticsearch Cloud cluster ID

            api_key (str): API key for authentication# Handle duplicate hostnames by adding suffix

        """duplicates = df['hostname'].duplicated(keep=False)

        self.es = Elasticsearch(if duplicates.any():

            cloud_id=cloud_id,    print(f"⚠️ Found {duplicates.sum()} duplicate hostnames, adding unique suffixes...")

            api_key=api_key,    for idx in df[duplicates].index:

            request_timeout=60,        df.loc[idx, 'hostname'] = f"{df.loc[idx, 'hostname']}_dup_{idx}"

            max_retries=3,

            retry_on_timeout=True# Fix date format from DD-MM-YYYY to YYYY-MM-DD

        )if 'operating_system_installation_date' in df.columns:

        self.index_name = "it_assets_index"    print("📅 Converting date format from DD-MM-YYYY to YYYY-MM-DD...")

            def convert_date_format(date_str):

    def verify_connection(self):        if pd.isna(date_str) or str(date_str).strip() == '':

        """            return None

        Verify Elasticsearch connection and log cluster information.        try:

                    # Parse DD-MM-YYYY and convert to YYYY-MM-DD

        Returns:            from datetime import datetime

            bool: True if connection successful, False otherwise            parsed_date = datetime.strptime(str(date_str).strip(), '%d-%m-%Y')

        """            return parsed_date.strftime('%Y-%m-%d')

        try:        except:

            info = self.es.info()            return None

            logger.info(f"Connected to Elasticsearch cluster: {info['cluster_name']}")    

            logger.info(f"Elasticsearch version: {info['version']['number']}")    df['operating_system_installation_date'] = df['operating_system_installation_date'].apply(convert_date_format)

            return True

        except Exception as e:cleaned_count = len(df)

            logger.error(f"Failed to connect to Elasticsearch: {e}")print(f"✅ Data cleaned: {initial_count} → {cleaned_count} records")

            return False

    # === CREATE INDEX WITH MAPPING ===

    def create_index_mapping(self):index_mapping = {

        """    "mappings": {

        Create index with optimized field mappings for IT asset data.        "properties": {

        """            "hostname": {"type": "keyword"},

        mapping = {            "country": {"type": "keyword"},

            "mappings": {            "operating_system_name": {"type": "keyword"},

                "properties": {            "operating_system_provider": {"type": "keyword"},

                    "hostname": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},            "operating_system_installation_date": {

                    "country": {"type": "keyword"},                "type": "date",

                    "region": {"type": "keyword"},                "format": "yyyy-MM-dd||strict_date_optional_time||epoch_millis"

                    "os_name": {"type": "keyword"},            },

                    "os_version": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},            "operating_system_lifecycle_status": {"type": "keyword"},

                    "os_install_date": {"type": "date", "format": "yyyy-MM-dd"},            "os_is_virtual": {"type": "keyword"},

                    "lifecycle_status": {"type": "keyword"},            "is_internet_facing": {"type": "keyword"},

                    "internet_facing": {"type": "boolean"},            "image_purpose": {"type": "keyword"},

                    "cpu_cores": {"type": "integer"},            "os_system_id": {"type": "keyword"},

                    "memory_gb": {"type": "float"},            "performance_score": {"type": "float"},

                    "disk_space_gb": {"type": "float"},            "indexed_at": {"type": "date"}

                    "network_speed_mbps": {"type": "integer"},        }

                    "uptime_days": {"type": "integer"},    }

                    "last_patched": {"type": "date", "format": "yyyy-MM-dd"},}

                    "indexed_at": {"type": "date"}

                }# Delete and recreate index for clean start

            }try:

        }    if es.indices.exists(index=TARGET_INDEX):

                es.indices.delete(index=TARGET_INDEX)

        try:        print(f"🗑️ Deleted existing index '{TARGET_INDEX}'")

            if self.es.indices.exists(index=self.index_name):    

                logger.info(f"Index '{self.index_name}' already exists")    es.indices.create(index=TARGET_INDEX, body=index_mapping)

                return True    print(f"✅ Created index '{TARGET_INDEX}' with proper mapping")

                except Exception as e:

            self.es.indices.create(index=self.index_name, body=mapping)    print(f"⚠️ Index management error: {e}")

            logger.info(f"Created index '{self.index_name}' with optimized mappings")

            return True# === PREPARE BULK DATA ===

            current_time = datetime.now().isoformat()

        except Exception as e:actions = []

            logger.error(f"Failed to create index: {e}")

            return Falsefor idx, row in df.iterrows():

        # Convert to dict and handle NaN values

    def load_and_validate_data(self, csv_file):    doc = row.to_dict()

        """    

        Load CSV data and perform validation checks.    # Replace NaN with None

            for key, value in doc.items():

        Args:        if pd.isna(value):

            csv_file (str): Path to the CSV file            doc[key] = None

                

        Returns:    # Add metadata

            pandas.DataFrame: Validated data or None if validation fails    doc['indexed_at'] = current_time

        """    doc['record_id'] = idx

        try:    

            # Load data with proper data types    action = {

            df = pd.read_csv(csv_file)        "_index": TARGET_INDEX,

            logger.info(f"Loaded {len(df)} records from {csv_file}")        "_id": doc['hostname'],

                    "_source": doc

            # Validate required columns    }

            required_columns = ['hostname', 'country', 'os_name']    actions.append(action)

            missing_columns = [col for col in required_columns if col not in df.columns]

            # === BULK UPLOAD WITH DETAILED ERROR HANDLING ===

            if missing_columns:try:

                logger.error(f"Missing required columns: {missing_columns}")    success_count, failed_items = helpers.bulk(

                return None        es, 

                    actions,

            # Data quality checks        chunk_size=100,

            null_hostnames = df['hostname'].isnull().sum()        request_timeout=60

            if null_hostnames > 0:    )

                logger.warning(f"Found {null_hostnames} records with null hostnames")    

                print(f"✅ Successfully uploaded {success_count} documents to index '{TARGET_INDEX}'")

            # Convert date fields    

            date_columns = ['os_install_date', 'last_patched']    # Verify indexing

            for col in date_columns:    import time

                if col in df.columns:    time.sleep(2)  # Wait for indexing to complete

                    df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')    doc_count = es.count(index=TARGET_INDEX)['count']

                print(f"🔍 Verification: Index contains {doc_count} documents")

            # Convert boolean fields    

            if 'internet_facing' in df.columns:except helpers.BulkIndexError as e:

                df['internet_facing'] = df['internet_facing'].map({'Yes': True, 'No': False})    print(f"❌ Bulk indexing errors occurred:")

                for error in e.errors[:5]:  # Show first 5 errors

            # Add indexing timestamp        print(f"   - {error}")

            df['indexed_at'] = datetime.now().isoformat()    print(f"   Total errors: {len(e.errors)}")

                

            logger.info("Data validation completed successfully")except Exception as e:

            return df    print(f"❌ Bulk upload failed: {e}") 
            
        except Exception as e:
            logger.error(f"Failed to load or validate data: {e}")
            return None
    
    def bulk_index_data(self, df):
        """
        Perform bulk indexing of asset data.
        
        Args:
            df (pandas.DataFrame): Data to index
            
        Returns:
            bool: True if indexing successful, False otherwise
        """
        try:
            # Prepare documents for bulk indexing
            actions = []
            for index, row in df.iterrows():
                doc = row.to_dict()
                # Remove any NaN values
                doc = {k: v for k, v in doc.items() if pd.notna(v)}
                
                action = {
                    "_index": self.index_name,
                    "_id": doc.get('hostname', f"asset_{index}"),
                    "_source": doc
                }
                actions.append(action)
            
            # Perform bulk indexing
            logger.info(f"Starting bulk indexing of {len(actions)} documents")
            success_count, failed_items = helpers.bulk(
                self.es,
                actions,
                chunk_size=100,
                request_timeout=60,
                max_retries=3,
                initial_backoff=2,
                max_backoff=600
            )
            
            if failed_items:
                logger.error(f"Failed to index {len(failed_items)} documents")
                for item in failed_items[:5]:  # Log first 5 failures
                    logger.error(f"Failed item: {item}")
            
            logger.info(f"Successfully indexed {success_count} documents")
            
            # Refresh index to make documents searchable
            self.es.indices.refresh(index=self.index_name)
            logger.info("Index refreshed - documents ready for search")
            
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Bulk indexing failed: {e}")
            return False
    
    def verify_indexing(self):
        """
        Verify that documents were indexed correctly.
        
        Returns:
            dict: Statistics about the indexed data
        """
        try:
            # Get index statistics
            stats = self.es.cat.count(index=self.index_name, format='json')[0]
            doc_count = int(stats['count'])
            
            # Sample a few documents
            sample_query = {
                "query": {"match_all": {}},
                "size": 3,
                "sort": [{"indexed_at": {"order": "desc"}}]
            }
            
            response = self.es.search(index=self.index_name, body=sample_query)
            sample_docs = response['hits']['hits']
            
            logger.info(f"Index verification complete:")
            logger.info(f"  - Total documents: {doc_count}")
            logger.info(f"  - Sample document count: {len(sample_docs)}")
            
            if sample_docs:
                logger.info("  - Sample document fields:")
                for field in sample_docs[0]['_source'].keys():
                    logger.info(f"    * {field}")
            
            return {
                'total_documents': doc_count,
                'sample_documents': len(sample_docs),
                'index_name': self.index_name
            }
            
        except Exception as e:
            logger.error(f"Index verification failed: {e}")
            return {}


def main():
    """
    Main execution function for IT asset indexing pipeline.
    """
    # Configuration - Replace with your actual credentials
    CLOUD_ID = "MyDeployment:YXNpYS1zb3V0aDEuZ2NwLmVsYXN0aWMtY2xvdWQuY29tJGYxOGQyMGE0OTlhZTQ4YzNhNDFjN2ZhNmZkZGNhM2ZhJDBlMGRhMGZmMjQyNDQ0OTNhYWFkOTJkNzg3YzFjZGRm"
    API_KEY = "VkpIVl9wTUIxTEk1SGx6YVZkRHU6UFFTa29KbzVTOGVlZmpGZG10WmttQQ=="
    CSV_FILE = "it_asset_inventory_cleaned.csv"
    
    logger.info("Starting IT Asset Inventory Indexing Pipeline")
    logger.info(f"Target CSV file: {CSV_FILE}")
    
    try:
        # Initialize indexer
        indexer = ITAssetIndexer(CLOUD_ID, API_KEY)
        
        # Verify connection
        if not indexer.verify_connection():
            logger.error("Cannot proceed without Elasticsearch connection")
            return False
        
        # Create index with optimized mapping
        if not indexer.create_index_mapping():
            logger.error("Failed to create index mapping")
            return False
        
        # Load and validate data
        df = indexer.load_and_validate_data(CSV_FILE)
        if df is None:
            logger.error("Data loading failed")
            return False
        
        # Perform bulk indexing
        if not indexer.bulk_index_data(df):
            logger.error("Bulk indexing failed")
            return False
        
        # Verify results
        stats = indexer.verify_indexing()
        if stats:
            logger.info("✅ IT Asset indexing pipeline completed successfully")
            logger.info(f"✅ Indexed {stats['total_documents']} IT assets")
            logger.info(f"✅ Ready for analytics and visualization in Kibana")
        else:
            logger.error("Index verification failed")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 IT Asset indexing completed successfully!")
        print("📊 Data is now ready for Kibana visualization")
        print("🔍 Access your Elasticsearch Cloud console to view the data")
    else:
        print("\n❌ IT Asset indexing failed")
        print("📋 Check the logs for detailed error information")