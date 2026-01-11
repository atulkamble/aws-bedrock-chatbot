"""
Diagnostic tool to check AWS Bedrock model access
"""

import boto3
import json
from botocore.exceptions import ClientError

def check_model_access():
    """Check which Bedrock models are available"""
    print("=" * 70)
    print("🔍 AWS Bedrock Model Access Diagnostic")
    print("=" * 70)
    
    try:
        # Create Bedrock client
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        print("\n✅ Connected to AWS Bedrock\n")
        
        # List foundation models
        print("📋 Checking available foundation models...")
        response = bedrock.list_foundation_models()
        
        available_models = []
        for model in response.get('modelSummaries', []):
            model_id = model.get('modelId', '')
            model_name = model.get('modelName', '')
            provider = model.get('providerName', '')
            
            # Filter for models we want to use
            if 'titan' in model_id.lower() or 'claude' in model_id.lower():
                available_models.append({
                    'id': model_id,
                    'name': model_name,
                    'provider': provider
                })
        
        if available_models:
            print(f"\n✅ Found {len(available_models)} models:")
            print("-" * 70)
            for model in available_models:
                print(f"  • {model['provider']}: {model['name']}")
                print(f"    ID: {model['id']}")
        else:
            print("\n⚠️  No Titan or Claude models found")
        
        # Now test actual invocation access
        print("\n" + "=" * 70)
        print("🧪 Testing Model Invocation Access")
        print("=" * 70)
        
        bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        test_models = [
            ('amazon.titan-text-express-v1', 'Amazon Titan Text Express'),
            ('anthropic.claude-3-haiku-20240307-v1:0', 'Claude 3 Haiku'),
            ('anthropic.claude-3-sonnet-20240229-v1:0', 'Claude 3 Sonnet'),
        ]
        
        accessible = []
        not_accessible = []
        
        for model_id, model_name in test_models:
            try:
                # Try a minimal invocation
                if 'titan' in model_id:
                    body = json.dumps({
                        "inputText": "Hello",
                        "textGenerationConfig": {"maxTokenCount": 10}
                    })
                else:
                    body = json.dumps({
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 10,
                        "messages": [{"role": "user", "content": "Hi"}]
                    })
                
                response = bedrock_runtime.invoke_model(
                    modelId=model_id,
                    body=body
                )
                
                accessible.append(model_name)
                print(f"\n✅ {model_name}")
                print(f"   Status: ACCESSIBLE")
                
            except ClientError as e:
                error_code = e.response['Error']['Code']
                error_msg = e.response['Error']['Message']
                not_accessible.append((model_name, error_code, error_msg))
                print(f"\n❌ {model_name}")
                print(f"   Status: NOT ACCESSIBLE")
                print(f"   Error: {error_code}")
                if "INVALID_PAYMENT_INSTRUMENT" in error_msg:
                    print(f"   Issue: Payment method needs verification")
                elif "AccessDenied" in error_code:
                    print(f"   Issue: Model access not enabled")
                else:
                    print(f"   Details: {error_msg[:100]}")
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 Summary")
        print("=" * 70)
        
        if accessible:
            print(f"\n✅ Accessible Models ({len(accessible)}):")
            for model in accessible:
                print(f"   • {model}")
        
        if not_accessible:
            print(f"\n❌ Not Accessible Models ({len(not_accessible)}):")
            for model, code, msg in not_accessible:
                print(f"   • {model}: {code}")
        
        # Recommendations
        print("\n" + "=" * 70)
        print("💡 Recommendations")
        print("=" * 70)
        
        if not accessible:
            print("\n📝 Actions to take:")
            
            has_payment_issue = any("INVALID_PAYMENT_INSTRUMENT" in msg for _, _, msg in not_accessible)
            has_access_issue = any("AccessDenied" in code for _, code, _ in not_accessible)
            
            if has_payment_issue:
                print("\n1. ⏰ WAIT: Payment verification in progress")
                print("   • Usually takes 5-15 minutes")
                print("   • Check: https://console.aws.amazon.com/billing/")
                print("   • Verify payment method shows as 'Verified'")
            
            if has_access_issue:
                print("\n2. ✅ ENABLE MODEL ACCESS:")
                print("   • Go to: https://console.aws.amazon.com/bedrock/")
                print("   • Click 'Model access' → 'Manage model access'")
                print("   • Enable: Amazon Titan and Anthropic Claude models")
                print("   • Click 'Request model access'")
                print("   • Wait for 'Access granted' status")
            
            print("\n3. 🔄 RUN THIS DIAGNOSTIC AGAIN:")
            print("   python check_models.py")
        else:
            print("\n✅ All tested models are accessible!")
            print("   Run: python app.py")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure:")
        print("  1. AWS credentials are configured (aws configure)")
        print("  2. You have permissions to access Bedrock")
        print("  3. You're in a supported region (us-east-1)")

if __name__ == "__main__":
    check_model_access()
