from elasticsearch import Elasticsearch
from datetime import datetime, date
import json

# Configuration
ES_ENDPOINT = "https://my-elasticsearch-project-e74838.es.asia-south1.gcp.elastic.cloud:443"
ES_API_KEY = "NXFiZUxwb0JOOUVTMksyeElqa0U6S051T2V2NnFJSlBaNW5ZOFZWaU5odw=="
SOURCE_INDEX = "it_assets_index"
TARGET_INDEX = "it_assets_enriched"

# === CONNECT TO ELASTICSEARCH ===
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

# === CREATE ENRICHED INDEX MAPPING ===
enriched_mapping = {
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
            "indexed_at": {"type": "date"},
            "record_id": {"type": "integer"},
            # New enriched fields
            "risk_level": {"type": "keyword"},
            "system_age_years": {"type": "integer"},
            "age_category": {"type": "keyword"},
            "compliance_status": {"type": "keyword"},
            "enriched_at": {"type": "date"}
        }
    }
}

# === DELETE AND CREATE TARGET INDEX ===
try:
    if es.indices.exists(index=TARGET_INDEX):
        es.indices.delete(index=TARGET_INDEX)
        print(f"🗑️ Deleted existing index '{TARGET_INDEX}'")
    
    es.indices.create(index=TARGET_INDEX, body=enriched_mapping)
    print(f"✅ Created enriched index '{TARGET_INDEX}'")
except Exception as e:
    print(f"❌ Error creating index: {e}")
    exit()

# === REINDEX WITH TRANSFORMATIONS ===
reindex_body = {
    "source": {
        "index": SOURCE_INDEX
    },
    "dest": {
        "index": TARGET_INDEX
    },
    "script": {
        "source": """
            // Calculate risk level based on lifecycle status
            if (ctx._source.operating_system_lifecycle_status != null) {
                String status = ctx._source.operating_system_lifecycle_status.toLowerCase();
                if (status.contains('eol') || status.contains('eos') || status.contains('end')) {
                    ctx._source.risk_level = 'High';
                } else if (status.contains('deprecated') || status.contains('unsupported')) {
                    ctx._source.risk_level = 'Medium';
                } else {
                    ctx._source.risk_level = 'Low';
                }
            } else {
                ctx._source.risk_level = 'Unknown';
            }
            
            // Calculate system age in years (simplified)
            if (ctx._source.operating_system_installation_date != null) {
                try {
                    String dateStr = ctx._source.operating_system_installation_date;
                    // Simple age calculation - assume current year 2025
                    if (dateStr.length() >= 4) {
                        int installYear = Integer.parseInt(dateStr.substring(0, 4));
                        int currentYear = 2025;
                        ctx._source.system_age_years = currentYear - installYear;
                        
                        // Categorize by age
                        int age = ctx._source.system_age_years;
                        if (age < 2) {
                            ctx._source.age_category = 'New';
                        } else if (age < 5) {
                            ctx._source.age_category = 'Mature';
                        } else {
                            ctx._source.age_category = 'Legacy';
                        }
                    } else {
                        ctx._source.system_age_years = 0;
                        ctx._source.age_category = 'Unknown';
                    }
                } catch (Exception e) {
                    ctx._source.system_age_years = 0;
                    ctx._source.age_category = 'Unknown';
                }
            } else {
                ctx._source.system_age_years = 0;
                ctx._source.age_category = 'Unknown';
            }
            
            // Determine compliance status
            if (ctx._source.risk_level == 'High' || ctx._source.age_category == 'Legacy') {
                ctx._source.compliance_status = 'Non-Compliant';
            } else if (ctx._source.risk_level == 'Medium') {
                ctx._source.compliance_status = 'At-Risk';
            } else {
                ctx._source.compliance_status = 'Compliant';
            }
            
            // Add enrichment timestamp
            ctx._source.enriched_at = '2025-11-02T00:00:00Z';
            
            // Skip records with missing hostnames or Unknown providers
            if (ctx._source.hostname == null || ctx._source.hostname == '' || 
                ctx._source.operating_system_provider == 'Unknown') {
                ctx.op = 'noop';
            }
        """,
        "lang": "painless"
    }
}

print("🔄 Starting reindexing with transformations...")

try:
    response = es.reindex(body=reindex_body, wait_for_completion=True, request_timeout=300)
    
    print(f"✅ Reindexing completed!")
    print(f"   - Total processed: {response.get('total', 0)}")
    print(f"   - Created: {response.get('created', 0)}")
    print(f"   - Updated: {response.get('updated', 0)}")
    print(f"   - Deleted: {response.get('deleted', 0)}")
    print(f"   - Time taken: {response.get('took', 0)}ms")
    
    if response.get('failures'):
        print(f"⚠️ Some failures occurred:")
        for failure in response['failures'][:3]:
            print(f"   - {failure}")
    
except Exception as e:
    print(f"❌ Reindexing failed: {e}")

# === VERIFY ENRICHED DATA ===
try:
    # Get document count
    doc_count = es.count(index=TARGET_INDEX)['count']
    print(f"🔍 Enriched index contains {doc_count} documents")
    
    # Sample a few documents to verify transformations
    sample_docs = es.search(
        index=TARGET_INDEX,
        body={
            "size": 3,
            "_source": ["hostname", "risk_level", "system_age_years", "age_category", "compliance_status"]
        }
    )
    
    print("\n📋 Sample enriched documents:")
    for doc in sample_docs['hits']['hits']:
        source = doc['_source']
        print(f"   • {source.get('hostname', 'N/A')} - Risk: {source.get('risk_level', 'N/A')}, "
              f"Age: {source.get('system_age_years', 'N/A')} years ({source.get('age_category', 'N/A')}), "
              f"Compliance: {source.get('compliance_status', 'N/A')}")
    
    # Get aggregation stats
    agg_response = es.search(
        index=TARGET_INDEX,
        body={
            "size": 0,
            "aggs": {
                "risk_levels": {
                    "terms": {"field": "risk_level"}
                },
                "compliance_status": {
                    "terms": {"field": "compliance_status"}
                },
                "age_categories": {
                    "terms": {"field": "age_category"}
                }
            }
        }
    )
    
    print("\n📊 Data Summary:")
    print("Risk Levels:")
    for bucket in agg_response['aggregations']['risk_levels']['buckets']:
        print(f"   • {bucket['key']}: {bucket['doc_count']} assets")
    
    print("Compliance Status:")
    for bucket in agg_response['aggregations']['compliance_status']['buckets']:
        print(f"   • {bucket['key']}: {bucket['doc_count']} assets")
    
    print("Age Categories:")
    for bucket in agg_response['aggregations']['age_categories']['buckets']:
        print(f"   • {bucket['key']}: {bucket['doc_count']} assets")
        
except Exception as e:
    print(f"⚠️ Error verifying data: {e}")

print("\n🎉 Data transformation and enrichment completed successfully!")