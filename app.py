"""
AWS Bedrock Chatbot Application
A simple chatbot using Amazon Bedrock models
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
        if model_id:
            self.model_id = model_id
        else:
            self.model_id = 'anthropic.claude-3-7-sonnet-20250219-v1:0'
        self.conversation_history = []
        
    def chat(self, user_message):
        """Send a message and get a response from the model"""
        try:
            # Prepare request based on model type
            is_titan = 'titan' in self.model_id.lower()
            
            if is_titan:
                # Amazon Titan format
                request_body = {
                    "inputText": user_message,
                    "textGenerationConfig": {
                        "maxTokenCount": 2000,
                        "temperature": 0.7,
                        "topP": 0.9
                    }
                }
            else:
                # Claude format with conversation history
                self.conversation_history.append({
                    "role": "user",
                    "content": user_message
                })
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
            
            if is_titan:
                # Titan response format
                assistant_message = response_body['results'][0]['outputText']
            else:
                # Claude response format
                assistant_message = response_body['content'][0]['text']
                # Add assistant response to history for Claude
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
                return "⚠️ Payment method verification pending (wait 5-15 min)"
            
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
    print("🤖 AWS Bedrock Chatbot - Claude 3.7 Sonnet")
    print("=" * 60)
    print("\nCommands:")
    print("  - Type your message to chat")
    print("  - Type 'clear' to clear conversation history")
    print("  - Type 'exit' or 'quit' to end the session")
    print("=" * 60)
    
    # Initialize chatbot with available on-demand models
    models_to_try = [
        ('anthropic.claude-3-7-sonnet-20250219-v1:0', 'Claude 3.7 Sonnet'),
        ('anthropic.claude-3-5-sonnet-20241022-v2:0', 'Claude 3.5 Sonnet v2'),
        ('anthropic.claude-3-5-haiku-20241022-v1:0', 'Claude 3.5 Haiku'),
        ('anthropic.claude-3-sonnet-20240229-v1:0', 'Claude 3 Sonnet'),
        ('anthropic.claude-3-haiku-20240307-v1:0', 'Claude 3 Haiku'),
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
            if "⚠️" in test1 or "INVALID_PAYMENT_INSTRUMENT" in test1:
                print(f"❌ Payment verification pending")
                continue
            elif "AWS Error" in test1 or "Error:" in test1:
                print(f"❌ Not accessible")
                continue
            
            # Second test to confirm it's stable
            test2 = temp_chatbot.chat("Test")
            if "⚠️" in test2 or "INVALID_PAYMENT_INSTRUMENT" in test2:
                print(f"❌ Payment issue on second test")
                continue
            elif "AWS Error" in test2 or "Error:" in test2:
                print(f"❌ Unstable")
                continue
            
            # Model is working!
            chatbot = temp_chatbot
            chatbot.clear_history()  # Clear test messages
            working_model = model_name
            print(f"✅ Connected using {model_name}!\n")
            break
            
        except Exception as e:
            print(f"❌ Failed")
            continue
    
    if not chatbot:
        print("\n" + "=" * 60)
        print("❌ NO MODELS AVAILABLE")
        print("=" * 60)
        print("\nTroubleshooting steps:")
        print("\n1. ⏰ Wait 5-15 minutes after adding payment method")
        print("   AWS needs time to verify your payment")
        print("\n2. ✅ Enable Model Access:")
        print("   • Go to: https://console.aws.amazon.com/bedrock/")
        print("   • Click 'Model access' in left menu")
        print("   • Enable 'Amazon Titan' and 'Claude' models")
        print("   • Click 'Save changes'")
        print("\n3. 💳 Verify Payment Method:")
        print("   • Go to: https://console.aws.amazon.com/billing/")
        print("   • Check payment method shows as 'Verified'")
        print("\n4. 🔄 Try different region:")
        print("   • Some regions activate faster than others")
        print("   • Try us-west-2 or eu-west-1")
        print("\n5. 📞 If still failing after 15 minutes:")
        print("   • Contact AWS Support")
        print("   • Check AWS Service Health Dashboard")
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
