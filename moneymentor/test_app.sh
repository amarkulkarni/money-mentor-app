#!/bin/bash
# MoneyMentor - Automated Test Script

set -e

echo "============================================================"
echo "MoneyMentor - Automated Testing"
echo "============================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name=$1
    local test_command=$2
    
    echo -e "${YELLOW}Testing:${NC} $test_name"
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC} - $test_name"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC} - $test_name"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo "Step 1: Environment Checks"
echo "------------------------------------------------------------"

# Check Python
run_test "Python 3.9+ installed" "python3 --version | grep -E 'Python 3\.([9]|[1-9][0-9])'"

# Check Docker
run_test "Docker installed" "docker --version"

# Check OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  OPENAI_API_KEY not set${NC}"
    echo "Attempting to load from .env file..."
    if [ -f ".env" ]; then
        export $(cat .env | grep -v '^#' | xargs)
    fi
fi

run_test "OPENAI_API_KEY set" "[ ! -z \"$OPENAI_API_KEY\" ]"

echo ""
echo "Step 2: Dependencies Check"
echo "------------------------------------------------------------"

run_test "FastAPI installed" "python3 -c 'import fastapi'"
run_test "LangChain installed" "python3 -c 'import langchain'"
run_test "OpenAI installed" "python3 -c 'import openai'"
run_test "Qdrant client installed" "python3 -c 'import qdrant_client'"
run_test "PyMuPDF installed" "python3 -c 'import fitz'"

echo ""
echo "Step 3: Qdrant Connection"
echo "------------------------------------------------------------"

# Check if Qdrant is running
if curl -s http://localhost:6333 > /dev/null 2>&1; then
    run_test "Qdrant running" "true"
else
    echo -e "${YELLOW}⚠️  Qdrant not running. Starting...${NC}"
    docker run -d -p 6333:6333 --name moneymentor-qdrant qdrant/qdrant > /dev/null 2>&1
    sleep 3
    run_test "Qdrant started" "curl -s http://localhost:6333 > /dev/null"
fi

echo ""
echo "Step 4: Document Files"
echo "------------------------------------------------------------"

run_test "data/ directory exists" "[ -d data ]"

PDF_COUNT=$(ls data/*.pdf 2>/dev/null | wc -l | xargs)
TXT_COUNT=$(ls data/*.txt 2>/dev/null | wc -l | xargs)
TOTAL_FILES=$((PDF_COUNT + TXT_COUNT))

if [ $TOTAL_FILES -gt 0 ]; then
    echo -e "${GREEN}✅ PASS${NC} - Found $PDF_COUNT PDF(s) and $TXT_COUNT TXT file(s)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}❌ FAIL${NC} - No documents found in data/"
    ((TESTS_FAILED++))
fi

echo ""
echo "Step 5: Module Imports"
echo "------------------------------------------------------------"

cd app

run_test "data_loader module" "python3 -c 'from data_loader import DataLoader'"
run_test "vectorstore module" "python3 -c 'from vectorstore import get_qdrant_client'"
run_test "rag_pipeline module" "python3 -c 'from rag_pipeline import load_knowledge, get_finance_answer'"

echo ""
echo "Step 6: Functional Tests (if knowledge base loaded)"
echo "------------------------------------------------------------"

# Check if processed files exist
if [ -d "data/processed" ] && [ "$(ls -A data/processed/*.txt 2>/dev/null)" ]; then
    echo -e "${GREEN}✅${NC} Processed files found"
    
    # Try a simple query test (without actually calling OpenAI)
    echo "Note: Skipping live query test to avoid API costs"
    echo "To test queries, run: python rag_pipeline.py --query 'your question'"
else
    echo -e "${YELLOW}⚠️${NC}  No processed files found"
    echo "Run: python data_loader.py to extract text"
    echo "Then: python rag_pipeline.py to build index"
fi

cd ..

echo ""
echo "============================================================"
echo "Test Summary"
echo "============================================================"
echo -e "${GREEN}Passed:${NC} $TESTS_PASSED"
echo -e "${RED}Failed:${NC} $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Extract text: cd app && python data_loader.py"
    echo "  2. Build index: python rag_pipeline.py"
    echo "  3. Test query: python rag_pipeline.py --query 'What is budgeting?'"
    echo "  4. Start API: python main.py"
    echo "  5. Visit docs: http://localhost:8000/docs"
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please fix the issues above.${NC}"
    exit 1
fi

