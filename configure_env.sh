#!/bin/bash
# Simple helper to create .env file with necessary API keys and configuration.
# Prompts the user for values and writes them to .env in repository root.

set -e

read -p "Telegram BOT_TOKEN: " BOT_TOKEN
read -p "OpenAI API key (API): " API
read -p "API URL [https://api.openai.com/v1/chat/completions]: " API_URL
API_URL=${API_URL:-https://api.openai.com/v1/chat/completions}
read -p "Default GPT model [gpt-5]: " GPT_ENGINE
GPT_ENGINE=${GPT_ENGINE:-gpt-5}
read -p "Google API key (optional): " GOOGLE_API_KEY
read -p "Google CSE ID (optional): " GOOGLE_CSE_ID
read -p "Claude API key (optional): " claude_api_key
read -p "Groq API key (optional): " GROQ_API_KEY
read -p "Google AI API key (Gemini) (optional): " GOOGLE_AI_API_KEY
read -p "Vertex private key (optional): " VERTEX_PRIVATE_KEY
read -p "Vertex project ID (optional): " VERTEX_PROJECT_ID
read -p "Vertex client email (optional): " VERTEX_CLIENT_EMAIL
read -p "Admin user IDs (comma separated, optional): " ADMIN_LIST
read -p "Allowed group IDs (comma separated, optional): " GROUP_LIST

cat > .env <<EOV
BOT_TOKEN=${BOT_TOKEN}
API_URL=${API_URL}
API=${API}
GPT_ENGINE=${GPT_ENGINE}
GOOGLE_API_KEY=${GOOGLE_API_KEY}
GOOGLE_CSE_ID=${GOOGLE_CSE_ID}
claude_api_key=${claude_api_key}
GROQ_API_KEY=${GROQ_API_KEY}
GOOGLE_AI_API_KEY=${GOOGLE_AI_API_KEY}
VERTEX_PRIVATE_KEY=${VERTEX_PRIVATE_KEY}
VERTEX_PROJECT_ID=${VERTEX_PROJECT_ID}
VERTEX_CLIENT_EMAIL=${VERTEX_CLIENT_EMAIL}
ADMIN_LIST=${ADMIN_LIST}
GROUP_LIST=${GROUP_LIST}
EOV

echo ".env configuration written."
