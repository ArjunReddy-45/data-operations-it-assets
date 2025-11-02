import pandas as pd
from elasticsearch import Elasticsearch, helpers
import logging
from datetime import datetime, timedelta
import json

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('transformation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ITAssetTransformer:
    """
    Advanced IT asset data transformation and risk assessment engine.
    """
    
    def __init__(self, cloud_id, api_key):
        """
        Initialize Elasticsearch connection for data transformation.
        
        Args:
            cloud_id (str): Elasticsearch Cloud cluster ID
            api_key (str): API key for authentication
        """
        self.es = Elasticsearch(
            cloud_id=cloud_id,
            api_key=api_key,
            request_timeout=60,
            max_retries=3,
            retry_on_timeout=True
        )
        self.source_index = "it_assets_index"
        self.target_index = "it_assets_enhanced"
        
        # Risk assessment configuration
        self.eol_eos_dates = {
            "Windows Server 2012": "2023-10-10",
            "Windows Server 2016": "2027-01-12",
            "Ubuntu 18.04": "2023-05-31",
            "CentOS 7": "2024-06-30",
            "Windows 10": "2025-10-14"
        }
        
        self.high_risk_countries = ["UNKNOWN", "CHINA", "RUSSIA", "IRAN"]
        self.critical_vendors = ["Microsoft", "Red Hat", "Canonical", "Oracle"]
    
    def transform_and_enhance_data(self):
        """
        Main transformation function that processes all documents.
        
        Returns:
            bool: True if transformation successful, False otherwise
        """
        try:
            logger.info("Starting comprehensive data transformation and risk assessment")
            
            # Create enhanced index mapping
            mapping = {
                "mappings": {
                    "properties": {
                        "hostname": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                        "country": {"type": "keyword"},
                        "os_name": {"type": "keyword"},
                        "os_version": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                        "internet_facing": {"type": "boolean"},
                        "eol_eos_risk": {"type": "keyword"},
                        "risk_category": {"type": "keyword"},
                        "overall_risk_score": {"type": "integer"},
                        "transformed_at": {"type": "date"}
                    }
                }
            }
            
            # Create target index
            if self.es.indices.exists(index=self.target_index):
                self.es.indices.delete(index=self.target_index)
                
            self.es.indices.create(index=self.target_index, body=mapping)
            logger.info(f"Created enhanced index '{self.target_index}'")
            
            # Use update_by_query for efficient transformation
            script = """
            // Calculate EOL/EOS Risk
            if (ctx._source.os_name != null && ctx._source.os_version != null) {
                String fullOsName = ctx._source.os_name + " " + ctx._source.os_version;
                if (fullOsName.toLowerCase().contains("windows server 2012") ||
                    fullOsName.toLowerCase().contains("ubuntu 18.04") ||
                    fullOsName.toLowerCase().contains("centos 7")) {
                    ctx._source.eol_eos_risk = "CRITICAL";
                } else if (fullOsName.toLowerCase().contains("windows 10")) {
                    ctx._source.eol_eos_risk = "HIGH";
                } else {
                    ctx._source.eol_eos_risk = "LOW";
                }
            } else {
                ctx._source.eol_eos_risk = "UNKNOWN";
            }
            
            // Calculate Geographic Risk
            if (ctx._source.country == null || ctx._source.country.equals("UNKNOWN")) {
                ctx._source.geographic_risk = "CRITICAL";
            } else {
                ctx._source.geographic_risk = "LOW";
            }
            
            // Calculate Business Criticality
            int criticalityScore = 0;
            if (ctx._source.internet_facing != null && ctx._source.internet_facing) {
                criticalityScore += 3;
            }
            if (ctx._source.cpu_cores != null && ctx._source.cpu_cores >= 8) {
                criticalityScore += 2;
            }
            if (ctx._source.memory_gb != null && ctx._source.memory_gb >= 32) {
                criticalityScore += 2;
            }
            
            if (criticalityScore >= 5) {
                ctx._source.business_criticality = "CRITICAL";
            } else if (criticalityScore >= 3) {
                ctx._source.business_criticality = "HIGH";
            } else if (criticalityScore >= 1) {
                ctx._source.business_criticality = "MEDIUM";
            } else {
                ctx._source.business_criticality = "LOW";
            }
            
            // Calculate Overall Risk Score
            Map riskWeights = ["CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1, "UNKNOWN": 2];
            int totalScore = riskWeights.get(ctx._source.eol_eos_risk) * 3 + 
                           riskWeights.get(ctx._source.geographic_risk) * 1 + 
                           riskWeights.get(ctx._source.business_criticality) * 2;
                           
            ctx._source.overall_risk_score = (int)((totalScore / 24.0) * 100);
            
            // Set Risk Category
            if (ctx._source.overall_risk_score >= 75) {
                ctx._source.risk_category = "CRITICAL";
            } else if (ctx._source.overall_risk_score >= 60) {
                ctx._source.risk_category = "HIGH";
            } else if (ctx._source.overall_risk_score >= 40) {
                ctx._source.risk_category = "MEDIUM";
            } else {
                ctx._source.risk_category = "LOW";
            }
            
            // Add timestamp
            ctx._source.transformed_at = new Date().getTime();
            
            // Filter out Unknown hostnames during processing
            if (ctx._source.hostname != null && ctx._source.hostname.toLowerCase().equals("unknown")) {
                ctx.op = "noop";
            }
            """
            
            # Execute the transformation using reindex
            reindex_body = {
                "source": {
                    "index": self.source_index,
                    "query": {
                        "bool": {
                            "must_not": {
                                "term": {
                                    "hostname.keyword": "Unknown"
                                }
                            }
                        }
                    }
                },
                "dest": {
                    "index": self.target_index
                },
                "script": {
                    "source": script,
                    "lang": "painless"
                }
            }
            
            logger.info("Executing data transformation with Painless script...")
            result = self.es.reindex(body=reindex_body, wait_for_completion=True)
            
            if result.get('took'):
                logger.info(f"Transformation completed in {result['took']}ms")
                logger.info(f"Created: {result.get('created', 0)} enhanced documents")
                
                # Refresh the index
                self.es.indices.refresh(index=self.target_index)
                
                return result.get('created', 0) > 0
            else:
                logger.error("Transformation failed - no result returned")
                return False
                
        except Exception as e:
            logger.error(f"Data transformation failed: {e}")
            return False


def main():
    """
    Main execution function for IT asset transformation pipeline.
    """
    # Configuration
    CLOUD_ID = "MyDeployment:YXNpYS1zb3V0aDEuZ2NwLmVsYXN0aWMtY2xvdWQuY29tJGYxOGQyMGE0OTlhZTQ4YzNhNDFjN2ZhNmZkZGNhM2ZhJDBlMGRhMGZmMjQyNDQ0OTNhYWFkOTJkNzg3YzFjZGRm"
    API_KEY = "VkpIVl9wTUIxTEk1SGx6YVZkRHU6UFFTa29KbzVTOGVlZmpGZG10WmttQQ=="
    
    logger.info("Starting IT Asset Enhancement & Risk Assessment Pipeline")
    
    try:
        # Initialize transformer
        transformer = ITAssetTransformer(CLOUD_ID, API_KEY)
        
        # Transform and enhance data
        if transformer.transform_and_enhance_data():
            logger.info("✅ IT Asset transformation pipeline completed successfully")
            return True
        else:
            logger.error("Data transformation failed")
            return False
        
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 IT Asset transformation completed successfully!")
        print("📊 Enhanced data with risk assessment is ready")
        print("🎯 Executive dashboards can now be created in Kibana")
        print("🚀 Access the 'it_assets_enhanced' index for advanced analytics")
    else:
        print("\n❌ IT Asset transformation failed")
        print("📋 Check the logs for detailed error information")