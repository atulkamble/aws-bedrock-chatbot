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
    for model_id, model_name in models_to_try:
        try:
            print(f"\n🔄 Trying {model_name}...")
            temp_chatbot = BedrockChatbot(model_id=model_id)
            
            # Test the model with a simple request
            test_response = temp_chatbot.chat("Hi")
            if "AWS Error" not in test_response and "Error:" not in test_response:
                chatbot = temp_chatbot
                print(f"✅ Connected successfully using {model_name}!\n")
                break
            else:
                print(f"❌ {model_name} not accessible: {test_response}")
                temp_chatbot.clear_history()
        except Exception as e:
            print(f"❌ {model_name} failed: {str(e)}")
    
    if not chatbot:
        print("\n❌ Could not connect to any Claude models.")
        print("\nPlease enable model access:")
        print("  1. Go to AWS Console → Bedrock → Model access")
        print("  2. Request access for Claude models")
        print("  3. Fill out the use case form")
        print("  4. Wait for approval (usually instant)")
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
