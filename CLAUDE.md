# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a CrowdWorks FAQ search system that uses AI to answer user support questions in Japanese. The system combines vector search with GPT-3.5-turbo to provide contextual answers from a FAQ database, deployed as an AWS Lambda function.

## Commands

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Build vector index from FAQ data
python create_index.py

# Test locally
python handler.py
python chat.py
```

### Deployment
```bash
# Deploy to AWS Lambda
serverless deploy

# Remove deployment
serverless remove
```

### Docker (for local testing)
```bash
# Build container
docker build -t cw-faq-search .

# Run container
docker run -p 8080:8080 -e OPENAI_API_KEY=your_key cw-faq-search
```

## Architecture

### Core Components

**handler.py** - AWS Lambda entry point
- Processes HTTP requests with query parameters or JSON body
- Returns FAQ answers as plain text responses

**chat.py** - Main search logic
- Loads pre-built vector index from `data/index/`
- Uses LlamaIndex for semantic search + GPT completion
- Implements Japanese prompt templates for FAQ context

**create_index.py** - Vector index generation
- Reads FAQ data from `data/cw_faq.json`
- Creates OpenAI embeddings and persists to `data/index/`

**data/cw_faq.json** - FAQ database (738KB)
- Contains Japanese FAQ entries with structure: `{"タイトル": title, "本文": content, "URL名": url, "カテゴリ番号": category}`

### Tech Stack
- **LangChain 0.0.188** + **LlamaIndex 0.6.16.post1** for LLM application framework
- **OpenAI API 0.27.7** for GPT-3.5-turbo and embeddings
- **AWS Lambda** with Docker containers (ARM64)
- **Serverless Framework** for deployment

### Data Flow
1. Query received via Lambda Function URL
2. Vector search against pre-built FAQ index
3. Retrieved context + query sent to GPT-3.5-turbo
4. Japanese response returned with relevant URLs

## Key Configuration

### Environment Variables
- `OPENAI_API_KEY` - Required for OpenAI API access

### Serverless Configuration (serverless.yml)
- Region: ap-northeast-1
- Architecture: ARM64  
- Timeout: 25 seconds
- Function URL enabled for direct HTTP access

### Docker Deployment
- Base: `public.ecr.aws/lambda/python:3`
- Pre-builds and includes vector indices for fast startup
- Entry point: `handler.faq_qa`

## API Usage

### Request Examples
```bash
# JSON body
curl -H "Content-type: application/json" -d '{"query":"メールアドレスを変更したい"}' 'https://your-api.lambda-url.ap-northeast-1.on.aws/'

# Query parameter  
curl 'https://your-api.lambda-url.ap-northeast-1.on.aws/?query=メールアドレスを変更したい'
```

### Response Format
Returns plain text with FAQ answer and relevant URLs in Japanese.

## Development Notes

### Japanese Language Support
- All prompts, responses, and FAQ content are in Japanese
- Uses specialized prompt templates for Japanese FAQ context
- No additional Japanese text processing libraries required

### Vector Index Management
- Indices are pre-built and stored in `data/index/` directory
- Deployed with the application to avoid rebuild overhead
- Recreate indices by running `create_index.py` when FAQ data changes

### Testing Approach
- No formal test framework - testing done via Jupyter notebooks in `jupyter/`
- `in-context-learning-01.ipynb` contains main development and testing code
- Manual testing through direct function calls

### Performance Considerations
- Pre-built indices enable fast Lambda cold starts
- 25-second timeout accommodates OpenAI API calls
- ARM64 architecture for cost optimization