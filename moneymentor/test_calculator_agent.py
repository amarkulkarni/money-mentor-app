#!/usr/bin/env python3
"""
Test script for the financial calculator agent integration.

This demonstrates how the calculator agent can be:
1. Called directly from Python
2. Integrated with the main chat endpoint
"""
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from agents.finance_calculator_agent import run_calculation_query


def test_calculator_queries():
    """Test various calculator queries"""
    
    print("=" * 70)
    print("Financial Calculator Agent - Integration Tests")
    print("=" * 70)
    print()
    
    test_queries = [
        "If I invest $500 a month at 7% for 20 years, how much?",
        "What if I put away $200 per month at 5% for 10 years?",
        "Invest 1000 monthly at 8% for 25 years",
        "$1500/month at 6.5% return for 15 years",
        "How much money do I need?",  # Should fail - missing params
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"Test {i}: {query}")
        print("-" * 70)
        
        result = run_calculation_query(query)
        
        if result['success']:
            print(f"✅ Success!")
            print(f"📊 Result: ${result['result']:,.2f}")
            print(f"📝 Parameters: {result['parameters']}")
            print(f"\n{result['explanation']}")
        else:
            print(f"❌ Failed")
            print(f"Error: {result['explanation']}")
        
        print()
        print()


def demo_api_integration():
    """
    Show how this would be integrated with the main API endpoint.
    
    Pattern for integration in app/main.py:
    """
    print("=" * 70)
    print("Example: API Integration Pattern")
    print("=" * 70)
    print()
    
    integration_code = '''
# In app/main.py, enhance the /api/chat endpoint:

from agents.finance_calculator_agent import run_calculation_query

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """Enhanced chat endpoint with calculator support"""
    
    question = request.question.lower()
    
    # Check if this is a calculation query
    calculation_keywords = ['invest', 'save', 'calculate', 'how much', 'future value']
    is_calculation = any(keyword in question for keyword in calculation_keywords)
    
    if is_calculation:
        # Try the calculator first
        calc_result = run_calculation_query(request.question)
        
        if calc_result['success']:
            # Return calculator result
            return ChatResponse(
                answer=calc_result['explanation'],
                sources=[{
                    'source': 'financial_calculator',
                    'text': f"Parameters: {calc_result['parameters']}",
                    'relevance_score': 1.0
                }],
                query=request.question,
                model='calculator_agent'
            )
    
    # Fall back to RAG pipeline for other questions
    answer = get_finance_answer(request.question, k=request.k)
    return ChatResponse(**answer)
'''
    
    print(integration_code)
    print()


def test_edge_cases():
    """Test edge cases and error handling"""
    
    print("=" * 70)
    print("Edge Case Tests")
    print("=" * 70)
    print()
    
    edge_cases = [
        ("Very long term", "Invest $100 monthly at 7% for 50 years"),
        ("Zero interest", "Save $500 per month at 0% for 10 years"),
        ("High contribution", "$10000 a month at 6% for 20 years"),
        ("Decimal rate", "$300 monthly at 7.25% for 15 years"),
        ("Missing years", "$500 a month at 7%"),  # Should fail
    ]
    
    for name, query in edge_cases:
        print(f"{name}: {query}")
        result = run_calculation_query(query)
        
        if result['success']:
            print(f"  ✅ ${result['result']:,.2f}")
        else:
            print(f"  ❌ Could not parse")
        print()


if __name__ == "__main__":
    test_calculator_queries()
    demo_api_integration()
    test_edge_cases()
    
    print("=" * 70)
    print("✅ All tests complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Integrate with /api/chat endpoint (see pattern above)")
    print("2. Add calculator button to frontend UI")
    print("3. Consider adding more calculators (loan, retirement, budget)")
    print()

