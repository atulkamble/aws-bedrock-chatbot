"""
Test script to verify AWS Bedrock connectivity
"""

import boto3
import json
from botocore.exceptions import ClientError

def test_bedrock_connection():
    """Test AWS Bedrock connection and model access"""
    print("🔍 Testing AWS Bedrock Connection...\n")
    
    try:
        # Create Bedrock client
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        print("✅ Successfully connected to AWS Bedrock")
        
        # List available models
        print("\n📋 Checking available foundation models...")
        bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        # Test with a simple invocation
        print("\n🧪 Testing connection to Claude 3 Sonnet...")
        model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
        
        test_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "messages": [
                {
                    "role": "user",
                    "content": "Say hello!"
                }
            ]
        }
        
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(test_body)
        )
        print("✅ Connection successful!")
        
    except Exception as e:
        print(f"❌ Connection test failed: {str(e)}")
        print("\nPlease ensure:")
        print("  1. You have AWS credentials configured")
        print("  2. You have access to Amazon Bedrock")
        print("  3. The Claude 3 Sonnet model is enabled in your region")

if __name__ == "__main__":
    test_bedrock_connection()
