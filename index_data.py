from elasticsearch import Elasticsearch, helpers
import pandas as pd
import os
import uuid
from datetime import datetime

ES_ENDPOINT = "https://my-elasticsearch-project-e74838.es.asia-south1.gcp.elastic.cloud:443"
ES_API_KEY = "NXFiZUxwb0JOOUVTMksyeElqa0U6S051T2V2NnFJSlBaNW5ZOFZWaU5odw=="
CSV_FILE = "C:/Users/ArjunReddyTadi/Desktop/mylearning/it_asset_inventory_cleaned.csv"
TARGET_INDEX = "miniproject_index"

# === CONNECT TO ELASTIC ===
es = Elasticsearch(
    ES_ENDPOINT,
    api_key=ES_API_KEY,
    verify_certs=True
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

# === DATA CLEANING ===
print("🧹 Cleaning data...")

# Remove empty/unnamed columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
print(f"✂️ Removed unnamed columns, now have {len(df.columns)} columns")

# Remove rows with null hostnames (if hostname exists)
initial_count = len(df)
if 'hostname' in df.columns:
    df = df.dropna(subset=['hostname'])
    cleaned_count = len(df)
    if initial_count != cleaned_count:
        print(f"🗑️ Removed {initial_count - cleaned_count} records with null hostnames")

print(f"✅ Data cleaned: {len(df)} records ready for indexing")
print(f"📊 Columns: {list(df.columns)}")

# === PREPARE BULK DATA WITH DETAILED ERROR HANDLING ===
current_time = datetime.now().isoformat()
actions = []

for idx, row in df.iterrows():
    # Convert row to dict and handle NaN values
    doc = row.to_dict()
    
    # Replace NaN values with None (null in JSON)
    for key, value in doc.items():
        if pd.isna(value):
            doc[key] = None
    
    # Add metadata
    doc['indexed_at'] = current_time
    doc['record_id'] = idx
    
    # Use hostname as ID if available, otherwise use row index
    doc_id = str(doc.get('hostname', f"record_{idx}"))
    
    action = {
        "_index": TARGET_INDEX,
        "_id": doc_id,
        "_source": doc
    }
    actions.append(action)

print(f"📦 Prepared {len(actions)} documents for bulk upload")

# === BULK UPLOAD WITH DETAILED ERROR HANDLING ===
try:
    # Use bulk with error collection
    success_count, failed_items = helpers.bulk(
        es, 
        actions, 
        stats_only=False,
        chunk_size=50,
        request_timeout=120
    )
    
    print(f"✅ Successfully uploaded {success_count} documents to index '{TARGET_INDEX}'")
    
except helpers.BulkIndexError as e:
    print(f"❌ Bulk index error occurred:")
    print(f"   Successfully indexed: {len(actions) - len(e.errors)} documents")
    print(f"   Failed to index: {len(e.errors)} documents")
    
    # Show detailed errors
    print("\n🔍 First 5 errors for debugging:")
    for i, error in enumerate(e.errors[:5]):
        error_detail = error.get('index', error.get('create', {}))
        error_info = error_detail.get('error', {})
        doc_id = error_detail.get('_id', 'unknown')
        
        print(f"   Error {i+1} (Doc ID: {doc_id}):")
        print(f"     Type: {error_info.get('type', 'unknown')}")
        print(f"     Reason: {error_info.get('reason', 'unknown')}")
        if 'caused_by' in error_info:
            print(f"     Caused by: {error_info['caused_by'].get('reason', 'unknown')}")
        print()
    
    if len(e.errors) > 5:
        print(f"   ... and {len(e.errors) - 5} more errors")

except Exception as e:
    print(f"❌ Unexpected error during bulk upload: {e}")
    print(f"   Error type: {type(e).__name__}")

# === VERIFY INDEX ===
try:
    import time
    time.sleep(2)  # Wait for indexing to complete
    
    doc_count = es.count(index=TARGET_INDEX)['count']
    print(f"\n🔍 Verification: Index '{TARGET_INDEX}' contains {doc_count} documents")
    
except Exception as e:
    print(f"⚠️ Could not verify index: {e}") 