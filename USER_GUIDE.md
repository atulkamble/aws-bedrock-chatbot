# AWS Bedrock Chatbot - User Guide

## 🎯 Overview

This is a fully functional chatbot application powered by Amazon Bedrock and Claude 3 Sonnet. The chatbot maintains conversation history and provides an interactive command-line interface.

## 📋 Files Created

1. **app.py** - Main chatbot application with conversation history
2. **test_connection.py** - Connection test utility
3. **requirements.txt** - Python dependencies
4. **setup.sh** - Automated setup script
5. **.env.example** - Environment variable template

## 🚀 Quick Start

### Installation

```bash
# Run the setup script
chmod +x setup.sh
./setup.sh
```

Or manually:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Make sure your AWS credentials are configured:

```bash
aws configure
```

You'll need:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (us-east-1 recommended)
- Access to Amazon Bedrock
- Claude 3 Sonnet model enabled

### Running the Chatbot

```bash
# Activate virtual environment
source venv/bin/activate

# Run the chatbot
python app.py
```

### Testing Connection

Before running the chatbot, test your connection:

```bash
python test_connection.py
```

## 💬 Using the Chatbot

Once running, you can:

- **Chat**: Type any message and press Enter
- **Clear history**: Type `clear` to start a fresh conversation
- **Exit**: Type `exit` or `quit` to end the session

### Example Conversation

```
👤 You: What can you help me with?

🤖 Assistant: I can help you with a wide variety of tasks...

👤 You: Tell me a joke

🤖 Assistant: Sure! Here's one...
```

## 🏗️ Architecture

### Key Components

1. **BedrockChatbot Class**
   - Manages AWS Bedrock connection
   - Handles conversation history
   - Processes requests and responses

2. **Main Function**
   - Provides interactive CLI interface
   - Handles user input and commands
   - Error handling and graceful exits

### Model Configuration

- **Model**: Claude 3 Sonnet (`anthropic.claude-3-sonnet-20240229-v1:0`)
- **Max Tokens**: 2000
- **Temperature**: 0.7
- **Top P**: 0.9

## 🔧 Customization

### Change Model

Edit the `model_id` in `app.py`:

```python
self.model_id = 'anthropic.claude-3-haiku-20240307-v1:0'  # For faster responses
# or
self.model_id = 'anthropic.claude-3-opus-20240229-v1:0'   # For better quality
```

### Adjust Parameters

Modify the request body in the `chat()` method:

```python
request_body = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 4000,      # Increase for longer responses
    "temperature": 0.9,       # Higher = more creative
    "top_p": 0.95            # Nucleus sampling
}
```

### Change Region

```python
chatbot = BedrockChatbot(region_name='us-west-2')
```

## 🛠️ Troubleshooting

### Connection Issues

If you get connection errors:

1. Check AWS credentials: `aws configure list`
2. Verify Bedrock access in AWS Console
3. Ensure model is enabled in your region
4. Check IAM permissions

### Model Access

Enable model access:
1. Go to AWS Console → Bedrock
2. Click "Model access" in the left menu
3. Request access for Claude 3 Sonnet
4. Wait for approval (usually instant)

### Permission Errors

Your IAM user/role needs these permissions:
- `bedrock:InvokeModel`
- `bedrock:ListFoundationModels`

## 📊 Features

✅ **Conversation History**: Maintains context across messages  
✅ **Error Handling**: Graceful handling of AWS and network errors  
✅ **Interactive CLI**: User-friendly command-line interface  
✅ **Clear History**: Reset conversation anytime  
✅ **Keyboard Interrupt**: Safe exit with Ctrl+C  

## 🔐 Security Best Practices

- Never commit AWS credentials to Git
- Use IAM roles when running on AWS (EC2, Lambda, etc.)
- Store credentials securely using AWS Secrets Manager
- Rotate access keys regularly
- Use least-privilege IAM policies

## 📝 Requirements

- Python 3.8+
- AWS Account with Bedrock access
- boto3 library
- Valid AWS credentials

## 🎓 Learning Resources

- [Amazon Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Claude API Reference](https://docs.anthropic.com/claude/reference/)
- [Boto3 Bedrock Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)

## 📄 License

See LICENSE file for details.

## 👨‍💻 Author

Built with ❤️ by [Atul Kamble](https://github.com/atulkamble)

---

**Version**: 1.0.0  
**Last Updated**: January 2026
