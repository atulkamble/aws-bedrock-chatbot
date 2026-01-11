#!/bin/bash

echo "🚀 Setting up AWS Bedrock Chatbot..."
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the chatbot:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Configure AWS credentials: aws configure"
echo "  3. Run the chatbot: python app.py"
echo ""
