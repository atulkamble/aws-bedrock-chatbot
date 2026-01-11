# AWS Bedrock Chatbot - Architecture Diagram

## System Architecture

```mermaid
graph TB
    subgraph "User Interface"
        A[👤 User Terminal<br/>Interactive CLI]
    end
    
    subgraph "Application Layer"
        B[🐍 Python Application<br/>app.py]
        C[🔧 BedrockChatbot Class]
        D[💬 Conversation History<br/>Context Management]
    end
    
    subgraph "AWS SDK Layer"
        E[📦 boto3 SDK]
        F[🔐 AWS Credentials<br/>IAM Authentication]
    end
    
    subgraph "AWS Bedrock Service"
        G[🌐 Bedrock Runtime API<br/>us-east-1]
        H[🔄 Model Router]
    end
    
    subgraph "Foundation Models"
        I[🤖 Claude 3.7 Sonnet<br/>Primary Model]
        J[⚡ Claude 3.5 Sonnet v2<br/>Fallback 1]
        K[🚀 Claude 3.5 Haiku<br/>Fallback 2]
        L[📊 Amazon Titan<br/>Fallback 3]
    end
    
    subgraph "AWS Infrastructure"
        M[💳 AWS Billing<br/>Payment Method]
        N[🔑 Model Access Control<br/>IAM Permissions]
    end
    
    A -->|User Input| B
    B -->|Initialize| C
    C -->|Maintain| D
    C -->|API Call| E
    E -->|Authenticate| F
    E -->|InvokeModel| G
    G -->|Select Model| H
    H -->|Route Request| I
    H -->|If Unavailable| J
    H -->|If Unavailable| K
    H -->|If Unavailable| L
    I -->|Response| G
    J -->|Response| G
    K -->|Response| G
    L -->|Response| G
    G -->|JSON Response| E
    E -->|Parse| C
    C -->|Format| B
    B -->|Display| A
    
    M -.->|Validates| N
    N -.->|Grants Access| G
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style I fill:#c8e6c9
    style G fill:#f8bbd0
    style M fill:#ffccbc
```

## Component Details

### 1. User Interface Layer
- **Terminal CLI**: Interactive command-line interface
- **Input/Output**: Real-time message exchange
- **Commands**: chat, clear, exit/quit

### 2. Application Layer
- **app.py**: Main application entry point
- **BedrockChatbot Class**: Core chatbot logic
  - Model initialization
  - Request/response handling
  - Error management
- **Conversation History**: Maintains context for Claude models

### 3. AWS SDK Layer
- **boto3**: AWS SDK for Python
- **bedrock-runtime client**: Specialized Bedrock API client
- **Authentication**: Uses AWS credentials (IAM)

### 4. AWS Bedrock Service
- **Runtime API**: Model invocation endpoint
- **Region**: us-east-1 (configurable)
- **Model Router**: Automatic fallback system
- **Request/Response**: JSON-based communication

### 5. Foundation Models
- **Primary**: Claude 3.7 Sonnet (newest)
- **Fallback Chain**: 3.5 Sonnet v2 → 3.5 Haiku → Titan
- **Capabilities**: 
  - Natural language understanding
  - Context-aware responses
  - Multi-turn conversations

### 6. AWS Infrastructure
- **Billing**: Payment method validation
- **IAM**: Identity and access management
- **Model Access**: Permission-based model availability

## Data Flow Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant A as app.py
    participant C as BedrockChatbot
    participant B as boto3
    participant BR as Bedrock Runtime
    participant M as Claude Model
    
    U->>A: Enter message
    A->>C: chat(message)
    C->>C: Add to history
    C->>B: invoke_model()
    B->>BR: HTTP POST request
    BR->>BR: Validate credentials
    BR->>BR: Check model access
    BR->>M: Forward request
    M->>M: Generate response
    M->>BR: Return response
    BR->>B: JSON response
    B->>C: Parse response
    C->>C: Update history
    C->>A: Return text
    A->>U: Display response
```

## Error Handling Flow

```mermaid
flowchart TD
    A[Start: Invoke Model] --> B{Model Available?}
    B -->|Yes| C{Payment Valid?}
    B -->|No| D[Try Next Model]
    C -->|Yes| E{Access Granted?}
    C -->|No| F[Payment Error]
    E -->|Yes| G[Success: Return Response]
    E -->|No| H[Access Denied Error]
    D --> I{More Models?}
    I -->|Yes| B
    I -->|No| J[All Models Failed]
    F --> K[Display Payment Instructions]
    H --> K
    J --> K
    K --> L[End]
    G --> L
    
    style G fill:#4caf50
    style J fill:#f44336
    style K fill:#ff9800
```

## Security Architecture

```mermaid
graph LR
    subgraph "Local Environment"
        A[AWS CLI Config<br/>~/.aws/credentials]
        B[Python Application]
    end
    
    subgraph "AWS IAM"
        C[Access Keys<br/>Access Key ID<br/>Secret Access Key]
        D[IAM Permissions<br/>bedrock:InvokeModel<br/>bedrock:ListFoundationModels]
    end
    
    subgraph "AWS Bedrock"
        E[Model Access Control]
        F[Payment Validation]
        G[API Endpoints]
    end
    
    A -->|Provides| C
    B -->|Reads| A
    C -->|Validates| D
    D -->|Grants| E
    F -->|Required for| E
    E -->|Allows| G
    B -->|Calls| G
    
    style A fill:#ffeb3b
    style D fill:#03a9f4
    style E fill:#4caf50
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Development Environment"
        A[💻 macOS Local Machine]
        B[🐍 Python 3.14<br/>Virtual Environment]
        C[📦 Dependencies<br/>boto3, botocore]
    end
    
    subgraph "Configuration"
        D[🔐 AWS Credentials<br/>~/.aws/credentials]
        E[⚙️ AWS Config<br/>~/.aws/config]
        F[📝 .env File<br/>Optional Settings]
    end
    
    subgraph "Application Files"
        G[app.py<br/>Main Application]
        H[check_models.py<br/>Diagnostics]
        I[test_connection.py<br/>Connection Test]
    end
    
    subgraph "AWS Cloud"
        J[🌐 AWS Bedrock<br/>us-east-1]
        K[🤖 Foundation Models]
    end
    
    A --> B
    B --> C
    A --> D
    A --> E
    A --> F
    B --> G
    B --> H
    B --> I
    G --> J
    H --> J
    I --> J
    J --> K
    
    style A fill:#e3f2fd
    style J fill:#fff3e0
    style K fill:#e8f5e9
```

## Model Selection Logic

```mermaid
flowchart TD
    Start[Application Start] --> Init[Initialize Model List]
    Init --> Try1[Try Claude 3.7 Sonnet]
    
    Try1 --> Test1{Test Connection}
    Test1 -->|Success| Success[Use This Model]
    Test1 -->|Fail| Try2[Try Claude 3.5 Sonnet v2]
    
    Try2 --> Test2{Test Connection}
    Test2 -->|Success| Success
    Test2 -->|Fail| Try3[Try Claude 3.5 Haiku]
    
    Try3 --> Test3{Test Connection}
    Test3 -->|Success| Success
    Test3 -->|Fail| Try4[Try Claude 3 Sonnet]
    
    Try4 --> Test4{Test Connection}
    Test4 -->|Success| Success
    Test4 -->|Fail| Try5[Try Claude 3 Haiku]
    
    Try5 --> Test5{Test Connection}
    Test5 -->|Success| Success
    Test5 -->|Fail| NoModel[No Models Available]
    
    Success --> Chat[Start Chat Loop]
    NoModel --> Error[Display Troubleshooting]
    
    style Success fill:#4caf50
    style NoModel fill:#f44336
    style Chat fill:#2196f3
```

## Technical Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Language** | Python 3.14 | Application development |
| **AWS SDK** | boto3 1.42.25+ | AWS service integration |
| **API** | Bedrock Runtime | Model invocation |
| **Models** | Claude 3.x/3.5/3.7 | AI responses |
| **Authentication** | AWS IAM | Security & access control |
| **CLI** | Interactive Terminal | User interface |
| **Package Manager** | pip | Dependency management |
| **Environment** | venv | Isolation & reproducibility |

## Key Features

### ✅ Implemented
- Multi-model fallback system
- Conversation history management
- Real-time error handling
- Payment validation detection
- Model availability diagnostics
- Interactive CLI interface
- AWS credential integration
- Graceful degradation

### 🔄 Configuration Options
- Region selection (default: us-east-1)
- Model preference ordering
- Temperature & Top-P parameters
- Max token limits
- Retry logic

### 🛡️ Security Features
- AWS IAM authentication
- Credential file protection
- No hardcoded secrets
- Secure API communication
- Permission-based access control

---

## Getting Started

1. **Setup**: Run `./setup.sh`
2. **Configure**: Set AWS credentials
3. **Enable**: Activate models in AWS Console
4. **Test**: Run `python check_models.py`
5. **Chat**: Run `python app.py`

For detailed setup instructions, see [USER_GUIDE.md](USER_GUIDE.md)

---

**Version**: 1.0.0  
**Last Updated**: January 2026  
**Author**: Atul Kamble
