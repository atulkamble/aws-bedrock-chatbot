"""
AWS Bedrock Chatbot Application
A simple chatbot using Amazon Bedrock's Claude model
"""

import boto3
import json
import os
from botocore.exceptions import ClientError

class BedrockChatbot:
    def __init__(self, region_name='us-east-1', model_id=None):
        """Initialize the Bedrock chatbot with AWS credentials"""
        self.region_name = region_name
        self.bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=region_name
        )
        # Try Haiku first (faster, cheaper, often has quicker access)
        # Then Sonnet (balanced), then Opus (most capable)
        if model_id:
            self.model_id = model_id
        else:
            self.model_id = 'anthropic.claude-3-haiku-20240307-v1:0'
        self.conversation_history = []
        
    def chat(self, user_message):
        """Send a message and get a response from Claude"""
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            # Prepare the request body
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2000,
                "messages": self.conversation_history,
                "temperature": 0.7,
                "top_p": 0.9
            }
            
            # Invoke the model
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            # Parse the response
            response_body = json.loads(response['body'].read())
            assistant_message = response_body['content'][0]['text']
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            
            # Handle payment instrument error specifically
            if "INVALID_PAYMENT_INSTRUMENT" in error_message:
                print("\n" + "=" * 60)
                print("❌ AWS PAYMENT METHOD REQUIRED")
                print("=" * 60)
                print("\nYour AWS account needs a valid payment method.")
                print("\n🔧 Fix this in 5 minutes:")
                print("\n1. Open: https://console.aws.amazon.com/billing/")
                print("2. Click 'Payment methods' → 'Add a payment method'")
                print("3. Enter your credit/debit card details")
                print("4. Wait 2-5 minutes for verification")
                print("5. Run this chatbot again")
                print("\n💰 Cost: FREE for light usage (generous free tier)")
                print("   - First 10,000 Haiku requests/month FREE")
                print("   - First 1,000 Sonnet requests/month FREE")
                print("=" * 60)
                return "\n⚠️  Please add a payment method to continue (see instructions above)"
            
            return f"AWS Error ({error_code}): {error_message}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
        return "Conversation history cleared."

def main():
    """Main function to run the chatbot"""
    print("=" * 60)
    print("🤖 AWS Bedrock Chatbot with Claude 3")
    print("=" * 60)
    print("\nCommands:")
    print("  - Type your message to chat")
    print("  - Type 'clear' to clear conversation history")
    print("  - Type 'exit' or 'quit' to end the session")
    print("=" * 60)
    
    # Initialize chatbot with fallback models
    models_to_try = [
        ('anthropic.claude-3-haiku-20240307-v1:0', 'Claude 3 Haiku (Fast)'),
        ('anthropic.claude-3-sonnet-20240229-v1:0', 'Claude 3 Sonnet (Balanced)'),
        ('anthropic.claude-3-5-sonnet-20240620-v1:0', 'Claude 3.5 Sonnet (Best)')
    ]
    
    chatbot = None
    working_model = None
    
    for model_id, model_name in models_to_try:
        try:
            print(f"\n🔄 Trying {model_name}...")
            temp_chatbot = BedrockChatbot(model_id=model_id)
            
            # Test with TWO messages to ensure it's really working
            test1 = temp_chatbot.chat("Hi")
            
            # Check for payment errors
            if "INVALID_PAYMENT_INSTRUMENT" in test1 or "⚠️" in test1:
                print(f"❌ Payment method required")
                continue
            elif "AWS Error" in test1 or "Error:" in test1:
                print(f"❌ Access denied or not available")
                continue
            
            # Second test to confirm it's stable
            test2 = temp_chatbot.chat("Test")
            if "INVALID_PAYMENT_INSTRUMENT" in test2 or "⚠️" in test2:
                print(f"❌ Payment validation failed on second test")
                continue
            elif "AWS Error" in test2 or "Error:" in test2:
                print(f"❌ Unstable connection")
                continue
            
            # Model is working!
            chatbot = temp_chatbot
            chatbot.clear_history()  # Clear test messages
            working_model = model_name
            print(f"✅ Successfully validated {model_name}!\n")
            break
            
        except Exception as e:
            print(f"❌ Failed: {str(e)[:50]}")
            continue
    
    if not chatbot:
        print("\n" + "=" * 60)
        print("❌ PAYMENT METHOD REQUIRED")
        print("=" * 60)
        print("\nAWS Bedrock requires a valid payment method.")
        print("\n📋 To fix this:")
        print("\n1. Go to: https://console.aws.amazon.com/billing/")
        print("2. Click 'Payment methods' in the left menu")
        print("3. Add a valid credit/debit card")
        print("4. Wait 2-5 minutes for AWS to verify")
        print("5. Run this chatbot again")
        print("\n💡 Note: AWS Bedrock has a free tier, but requires")
        print("   a payment method on file for billing purposes.")
        print("\n" + "=" * 60)
        return
    
    # Chat loop
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit']:
                print("\n👋 Goodbye! Thanks for chatting!")
                break
                
            if user_input.lower() == 'clear':
                print(f"\n🔄 {chatbot.clear_history()}")
                continue
            
            print("\n🤖 Assistant: ", end="", flush=True)
            response = chatbot.chat(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for chatting!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
