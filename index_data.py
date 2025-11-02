from elasticsearch import Elasticsearch, helpers
import pandas as pd
import os
from datetime import datetime
import json

# Configuration
ES_ENDPOINT = "https://my-elasticsearch-project-e74838.es.asia-south1.gcp.elastic.cloud:443"
ES_API_KEY = "NXFiZUxwb0JOOUVTMksyeElqa0U6S051T2V2NnFJSlBaNW5ZOFZWaU5odw=="
CSV_FILE = "C:/Users/ArjunReddyTadi/Desktop/mylearning/it_asset_inventory_cleaned.csv"
TARGET_INDEX = "it_assets_index"
# === CONNECT TO ELASTIC ===
es = Elasticsearch(
    ES_ENDPOINT,
    api_key=ES_API_KEY,
    verify_certs=False  # Temporary fix for SSL issues
)

# === CHECK CONNECTION ===
if not es.ping():
    print("❌ Connection failed! Please check endpoint or API key.")
    exit()
else:
    print("✅ Connected to Elasticsearch!")

# === READ CSV FILE ===
if not os.path.exists(CSV_FILE):
    print(f"❌ CSV file not found: {CSV_FILE}")
    exit()

df = pd.read_csv(CSV_FILE)
print(f"📄 Loaded {len(df)} records from {CSV_FILE}")

# === DATA VALIDATION AND CLEANING ===
print("🧹 Validating and cleaning data...")

# Remove rows with empty hostnames
initial_count = len(df)
df = df.dropna(subset=['hostname'])
df = df[df['hostname'].str.strip() != '']

# Remove unnamed columns if they exist
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Handle duplicate hostnames by adding suffix
duplicates = df['hostname'].duplicated(keep=False)
if duplicates.any():
    print(f"⚠️ Found {duplicates.sum()} duplicate hostnames, adding unique suffixes...")
    for idx in df[duplicates].index:
        df.loc[idx, 'hostname'] = f"{df.loc[idx, 'hostname']}_dup_{idx}"

cleaned_count = len(df)
print(f"✅ Data cleaned: {initial_count} → {cleaned_count} records")

# === CREATE INDEX WITH MAPPING ===
index_mapping = {
    "mappings": {
        "properties": {
            "hostname": {"type": "keyword"},
            "country": {"type": "keyword"},
            "operating_system_name": {"type": "keyword"},
            "operating_system_provider": {"type": "keyword"},
            "operating_system_installation_date": {
                "type": "date",
                "format": "yyyy-MM-dd||strict_date_optional_time||epoch_millis"
            },
            "operating_system_lifecycle_status": {"type": "keyword"},
            "os_is_virtual": {"type": "keyword"},
            "is_internet_facing": {"type": "keyword"},
            "image_purpose": {"type": "keyword"},
            "os_system_id": {"type": "keyword"},
            "performance_score": {"type": "float"},
            "indexed_at": {"type": "date"}
        }
    }
}

# Delete and recreate index for clean start
try:
    if es.indices.exists(index=TARGET_INDEX):
        es.indices.delete(index=TARGET_INDEX)
        print(f"🗑️ Deleted existing index '{TARGET_INDEX}'")
    
    es.indices.create(index=TARGET_INDEX, body=index_mapping)
    print(f"✅ Created index '{TARGET_INDEX}' with proper mapping")
except Exception as e:
    print(f"⚠️ Index management error: {e}")

# === PREPARE BULK DATA ===
current_time = datetime.now().isoformat()
actions = []

for idx, row in df.iterrows():
    # Convert to dict and handle NaN values
    doc = row.to_dict()
    
    # Replace NaN with None
    for key, value in doc.items():
        if pd.isna(value):
            doc[key] = None
    
    # Add metadata
    doc['indexed_at'] = current_time
    doc['record_id'] = idx
    
    action = {
        "_index": TARGET_INDEX,
        "_id": doc['hostname'],
        "_source": doc
    }
    actions.append(action)

# === BULK UPLOAD WITH DETAILED ERROR HANDLING ===
try:
    success_count, failed_items = helpers.bulk(
        es, 
        actions,
        chunk_size=100,
        request_timeout=60
    )
    
    print(f"✅ Successfully uploaded {success_count} documents to index '{TARGET_INDEX}'")
    
    # Verify indexing
    import time
    time.sleep(2)  # Wait for indexing to complete
    doc_count = es.count(index=TARGET_INDEX)['count']
    print(f"🔍 Verification: Index contains {doc_count} documents")
    
except helpers.BulkIndexError as e:
    print(f"❌ Bulk indexing errors occurred:")
    for error in e.errors[:5]:  # Show first 5 errors
        print(f"   - {error}")
    print(f"   Total errors: {len(e.errors)}")
    
except Exception as e:
    print(f"❌ Bulk upload failed: {e}") 