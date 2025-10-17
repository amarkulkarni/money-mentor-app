#!/bin/bash
# MoneyMentor Quick Start Script

set -e

echo "============================================================"
echo "MoneyMentor - Quick Start"
echo "============================================================"
echo ""

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY not set"
    echo ""
    echo "Please set your OpenAI API key:"
    echo "  export OPENAI_API_KEY='sk-your-key-here'"
    echo ""
    exit 1
fi

echo "✅ OpenAI API key found"

# Check if Qdrant is running
echo "Checking Qdrant connection..."
if curl -s http://localhost:6333 > /dev/null 2>&1; then
    echo "✅ Qdrant is running"
else
    echo "❌ Qdrant is not running"
    echo ""
    echo "Please start Qdrant:"
    echo "  docker run -p 6333:6333 qdrant/qdrant"
    echo ""
    exit 1
fi

echo ""
echo "Step 1: Extracting text from documents..."
echo "------------------------------------------------------------"
cd app
python data_loader.py

echo ""
echo "Step 2: Building embeddings and indexing..."
echo "------------------------------------------------------------"
python rag_pipeline.py

echo ""
echo "============================================================"
echo "✅ Setup Complete!"
echo "============================================================"
echo ""
echo "You can now:"
echo "  1. Start the API server: python main.py"
echo "  2. Test a query: python rag_pipeline.py --query 'your question'"
echo "  3. Visit the API docs: http://localhost:8000/docs"
echo ""

