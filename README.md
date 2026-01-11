<div align="center">
<h1>🚀 MyApp</h1>
<p><strong>Built with ❤️ by <a href="https://github.com/atulkamble">Atul Kamble</a></strong></p>

<p>
<a href="https://codespaces.new/atulkamble/template.git">
<img src="https://github.com/codespaces/badge.svg" alt="Open in GitHub Codespaces" />
</a>
<a href="https://vscode.dev/github/atulkamble/template">
<img src="https://img.shields.io/badge/Open%20with-VS%20Code-007ACC?logo=visualstudiocode&style=for-the-badge" alt="Open with VS Code" />
</a>
<a href="https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/atulkamble/template">
<img src="https://img.shields.io/badge/Dev%20Containers-Ready-blue?logo=docker&style=for-the-badge" />
</a>
<a href="https://desktop.github.com/">
<img src="https://img.shields.io/badge/GitHub-Desktop-6f42c1?logo=github&style=for-the-badge" />
</a>
</p>

<p>
<a href="https://github.com/atulkamble">
<img src="https://img.shields.io/badge/GitHub-atulkamble-181717?logo=github&style=flat-square" />
</a>
<a href="https://www.linkedin.com/in/atuljkamble/">
<img src="https://img.shields.io/badge/LinkedIn-atuljkamble-0A66C2?logo=linkedin&style=flat-square" />
</a>
<a href="https://x.com/atul_kamble">
<img src="https://img.shields.io/badge/X-@atul_kamble-000000?logo=x&style=flat-square" />
</a>
</p>

<strong>Version 1.0.0</strong> | <strong>Last Updated:</strong> January 2026
</div>

---

## 🧠 AWS Bedrock Chatbot – Full Project

![Image](https://d2908q01vomqb2.cloudfront.net/fc074d501302eb2b93e2554793fcaf50b3bf7291/2025/05/21/ARCHBLOG-1179-1-1260x559.jpg)

![Image](https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2024/05/15/ml-15933-archdiag-new2.png)

![Image](https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2024/07/15/solution-overview-v1.jpg)

![Image](https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2024/11/14/ML-17361-0-scaled.jpg)

### 🔗 Core Service

Powered by **Amazon Web Services – Amazon Bedrock**

---

## 📁 Repository Structure

```text
aws-bedrock-chatbot/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── bedrock_client.py
│   │   ├── schemas.py
│   │   └── config.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── streamlit_app.py
│   └── requirements.txt
│
├── infra/
│   ├── iam-policy.json
│   └── deploy.sh
│
├── .env.example
├── README.md
└── .gitignore
```

---

## 🔐 IAM Policy (Mandatory)

📄 `infra/iam-policy.json`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "*"
    }
  ]
}
```

Attach this policy to:

* EC2 Role / ECS Task Role / Lambda Role

---

## ⚙️ Backend – FastAPI + Bedrock

### `backend/app/config.py`

```python
import os

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv(
    "MODEL_ID",
    "anthropic.claude-3-sonnet-20240229-v1:0"
)
```

---

### `backend/app/bedrock_client.py`

```python
import boto3
import json
from app.config import AWS_REGION, MODEL_ID

bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)

def invoke_bedrock(prompt: str) -> str:
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    return response_body["content"][0]["text"]
```

---

### `backend/app/schemas.py`

```python
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
```

---

### `backend/app/main.py`

```python
from fastapi import FastAPI
from app.schemas import ChatRequest, ChatResponse
from app.bedrock_client import invoke_bedrock

app = FastAPI(title="AWS Bedrock Chatbot")

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = invoke_bedrock(request.message)
    return ChatResponse(reply=reply)
```

---

### `backend/requirements.txt`

```text
fastapi
uvicorn
boto3
python-dotenv
```

---

### `backend/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🎨 Frontend – Streamlit Chat UI

### `frontend/streamlit_app.py`

```python
import streamlit as st
import requests

API_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="AWS Bedrock Chatbot", layout="centered")
st.title("🤖 AWS Bedrock Chatbot")

user_input = st.text_input("Ask something:")

if st.button("Send") and user_input:
    response = requests.post(API_URL, json={"message": user_input})
    if response.status_code == 200:
        st.success(response.json()["reply"])
    else:
        st.error("Backend error")
```

---

### `frontend/requirements.txt`

```text
streamlit
requests
```

---

## 🌍 Environment Variables

### `.env.example`

```env
AWS_REGION=us-east-1
MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
AWS_PROFILE=default
```

---

## 🚀 Run Locally (Step-by-Step)

### 1️⃣ Enable Bedrock Model

AWS Console → **Bedrock → Model access → Enable Claude**

---

### 2️⃣ Start Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 3️⃣ Start Frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Frontend:
👉 [http://localhost:8501](http://localhost:8501)

---

## ☁️ Deployment Options

| Platform             | Supported |
| -------------------- | --------- |
| EC2                  | ✅         |
| ECS Fargate          | ✅         |
| EKS                  | ✅         |
| Lambda + API Gateway | ✅         |
| App Runner           | ✅         |

---

## 🧪 Sample API Test

```bash
curl -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-d '{"message":"Explain Kubernetes in simple terms"}'
```

---

## 📘 README.md (Short)

```md
# aws-bedrock-chatbot

Production-ready AI chatbot using Amazon Bedrock and Claude models.

## Stack
- Amazon Bedrock
- FastAPI
- Streamlit
- Docker

## Run
Backend: uvicorn app.main:app
Frontend: streamlit run streamlit_app.py
```

---
