"""
MoneyMentor - Financial Calculator Agent

Provides calculation tools for financial planning queries.
Includes future value calculations, investment projections, and more.
"""
import re
from typing import Dict, Any, Optional, Tuple


def calculate_future_value(
    monthly_contrib: float,
    annual_rate: float,
    years: int,
    compounds_per_year: int = 12
) -> Tuple[float, str]:
    """
    Calculate the future value of an annuity with periodic contributions.
    
    Uses the standard finance formula:
    FV = PMT × [((1 + r)^n - 1) / r]
    
    Where:
    - PMT = periodic payment (monthly contribution)
    - r = interest rate per period
    - n = total number of periods
    
    Args:
        monthly_contrib: Monthly contribution amount (e.g., 500 for $500/month)
        annual_rate: Annual interest rate as percentage (e.g., 7 for 7%)
        years: Number of years to invest
        compounds_per_year: Number of compounding periods per year (default: 12 for monthly)
        
    Returns:
        Tuple of (future_value, explanation_string)
        
    Example:
        >>> fv, explanation = calculate_future_value(500, 7, 20)
        >>> print(f"Future Value: ${fv:,.2f}")
        Future Value: $260,463.12
    """
    # Convert annual rate from percentage to decimal
    r = (annual_rate / 100) / compounds_per_year
    
    # Total number of periods
    n = years * compounds_per_year
    
    # Calculate future value
    if r == 0:
        # Special case: no interest
        future_value = monthly_contrib * n
    else:
        future_value = monthly_contrib * (((1 + r) ** n - 1) / r)
    
    # Calculate total contributions
    total_contributed = monthly_contrib * n
    
    # Calculate interest earned
    interest_earned = future_value - total_contributed
    
    # Create explanation
    explanation = (
        f"Investing ${monthly_contrib:,.2f}/month at {annual_rate}% annual return "
        f"for {years} years:\n"
        f"• Total contributions: ${total_contributed:,.2f}\n"
        f"• Interest earned: ${interest_earned:,.2f}\n"
        f"• Final value: ${future_value:,.2f}\n"
        f"Your money will grow {future_value / total_contributed:.2f}x through compound interest!"
    )
    
    return future_value, explanation


def parse_investment_query(query: str) -> Optional[Dict[str, float]]:
    """
    Parse natural language investment queries to extract parameters.
    
    Supports queries like:
    - "If I invest $500 a month at 7% for 20 years, how much?"
    - "Invest 1000 per month at 8% for 30 years"
    - "$200/month at 5% return for 10 years"
    - "500 monthly at 6.5% for 15 years"
    
    Args:
        query: Natural language query string
        
    Returns:
        Dictionary with 'monthly_contrib', 'annual_rate', 'years' or None if parsing fails
    """
    query = query.lower()
    
    # Pattern 1: Extract monthly contribution
    # Matches: $500, 500, $1,000, 1000, $10000, etc.
    monthly_patterns = [
        r'\$?(\d{1,10}(?:,\d{3})*(?:\.\d{2})?)\s*(?:per month|a month|monthly|/month|month)',
        r'invest\s+\$?(\d{1,10}(?:,\d{3})*(?:\.\d{2})?)',
        r'\$?(\d{1,10}(?:,\d{3})*(?:\.\d{2})?)\s*each month',
    ]
    
    monthly_contrib = None
    for pattern in monthly_patterns:
        match = re.search(pattern, query)
        if match:
            monthly_contrib = float(match.group(1).replace(',', ''))
            break
    
    # Pattern 2: Extract annual rate
    # Matches: 7%, 7.5%, at 7%, 7 percent
    rate_patterns = [
        r'(?:at|@|with|earning|return(?:ing)?)\s+(\d+(?:\.\d+)?)\s*%',
        r'(\d+(?:\.\d+)?)\s*%\s*(?:annual|yearly|per year)?',
        r'(\d+(?:\.\d+)?)\s*percent',
    ]
    
    annual_rate = None
    for pattern in rate_patterns:
        match = re.search(pattern, query)
        if match:
            annual_rate = float(match.group(1))
            break
    
    # Pattern 3: Extract years
    # Matches: 20 years, for 20 years, over 30 years
    year_patterns = [
        r'(?:for|over|in)\s+(\d+)\s*years?',
        r'(\d+)\s*years?',
    ]
    
    years = None
    for pattern in year_patterns:
        match = re.search(pattern, query)
        if match:
            years = int(match.group(1))
            break
    
    # Return None if any required parameter is missing
    if monthly_contrib is None or annual_rate is None or years is None:
        return None
    
    return {
        'monthly_contrib': monthly_contrib,
        'annual_rate': annual_rate,
        'years': years
    }


def parse_lump_sum_query(query: str) -> Optional[Dict[str, float]]:
    """
    Parse lump sum investment queries (one-time investments).
    
    Supports queries like:
    - "If I invest $1000 at 7% for 5 years"
    - "Invest 5000 at current rates for 10 years"
    - "$10,000 at 6.5% for 3 years"
    
    Args:
        query: Natural language query string
        
    Returns:
        Dictionary with 'principal', 'annual_rate', 'years' or None if parsing fails
    """
    query_lower = query.lower()
    
    # Check if it's NOT a monthly contribution
    monthly_indicators = ['per month', 'monthly', '/month', 'a month', 'each month']
    if any(indicator in query_lower for indicator in monthly_indicators):
        return None  # This is a monthly contribution, not lump sum
    
    # Pattern 1: Extract principal (lump sum amount)
    # Matches: invest $1000, I invest $5,000, $10000
    principal_patterns = [
        r'invest\s+\$?(\d{1,10}(?:,\d{3})*(?:\.\d{2})?)',
        r'\$(\d{1,10}(?:,\d{3})*(?:\.\d{2})?)\s+at',
        r'principal\s+(?:of\s+)?\$?(\d{1,10}(?:,\d{3})*(?:\.\d{2})?)',
    ]
    
    principal = None
    for pattern in principal_patterns:
        match = re.search(pattern, query_lower)
        if match:
            principal = float(match.group(1).replace(',', ''))
            break
    
    # Pattern 2: Extract annual rate
    # Try to get "current rates" from context or default
    rate_patterns = [
        r'(?:at|@|with|earning|return(?:ing)?)\s+(\d+(?:\.\d+)?)\s*%',
        r'(\d+(?:\.\d+)?)\s*%\s*(?:annual|yearly|per year)?',
        r'(\d+(?:\.\d+)?)\s*percent',
    ]
    
    annual_rate = None
    for pattern in rate_patterns:
        match = re.search(pattern, query_lower)
        if match:
            annual_rate = float(match.group(1))
            break
    
    # Check for "current rates" - this means we need live data
    if annual_rate is None and ('current' in query_lower or 'today' in query_lower):
        # Signal that this needs live rate lookup (will be handled by caller)
        annual_rate = -1  # Special flag for "needs live data"
    
    # Pattern 3: Extract years
    year_patterns = [
        r'(?:for|over|in)\s+(\d+)\s*years?',
        r'(\d+)\s*years?',
    ]
    
    years = None
    for pattern in year_patterns:
        match = re.search(pattern, query_lower)
        if match:
            years = int(match.group(1))
            break
    
    # Return None if any required parameter is missing
    if principal is None or years is None:
        return None
    
    return {
        'principal': principal,
        'annual_rate': annual_rate,
        'years': years
    }


def run_calculation_query(query: str) -> Dict[str, Any]:
    """
    High-level wrapper that parses natural language queries and returns calculations.
    
    Handles both:
    - Monthly contributions (annuity): "invest $500 per month"
    - Lump sum investments: "invest $1000" (one-time)
    
    This function:
    1. Parses the natural language query
    2. Extracts parameters (amount, rate, years)
    3. Calculates future value
    4. Returns structured result
    
    Args:
        query: Natural language query about investment calculations
        
    Returns:
        Dictionary with:
        - 'success': bool
        - 'result': float (future value) or None
        - 'explanation': str (detailed explanation or error message)
        - 'parameters': dict (extracted parameters) or None
        
    Examples:
        >>> result = run_calculation_query("If I invest $500 a month at 7% for 20 years, how much?")
        >>> print(f"${result['result']:,.2f}")
        $260,463.12
        
        >>> result = run_calculation_query("Invest $1000 at 7% for 5 years")
        >>> print(result['explanation'])
        Investing $1,000.00 at 7.0% annual return for 5 years (compounded 12x/year):
        ...
    """
    # Try parsing as lump sum first
    lump_sum_params = parse_lump_sum_query(query)
    
    if lump_sum_params:
        # Check if it needs live rate data
        if lump_sum_params['annual_rate'] == -1:
            return {
                'success': False,
                'result': None,
                'explanation': (
                    "I need a live interest rate to calculate this. "
                    "Please specify a rate or let me search for current rates."
                ),
                'parameters': lump_sum_params,
                'needs_live_data': True
            }
        
        # Calculate compound interest for lump sum
        try:
            future_value, explanation = calculate_compound_interest(
                principal=lump_sum_params['principal'],
                annual_rate=lump_sum_params['annual_rate'],
                years=lump_sum_params['years']
            )
            
            return {
                'success': True,
                'result': round(future_value, 2),
                'explanation': explanation,
                'parameters': lump_sum_params,
                'investment_type': 'lump_sum'
            }
            
        except Exception as e:
            return {
                'success': False,
                'result': None,
                'explanation': f"Error calculating lump sum: {str(e)}",
                'parameters': lump_sum_params
            }
    
    # Try parsing as monthly contribution
    params = parse_investment_query(query)
    
    if params is None:
        return {
            'success': False,
            'result': None,
            'explanation': (
                "I couldn't parse that query. Please try a format like:\n"
                "• Monthly: 'If I invest $500 a month at 7% for 20 years, how much?'\n"
                "• Lump sum: 'If I invest $1000 at 7% for 5 years, how much?'\n"
                "• '$200/month at 5% return for 10 years'"
            ),
            'parameters': None
        }
    
    # Calculate future value for monthly contributions
    try:
        future_value, explanation = calculate_future_value(
            monthly_contrib=params['monthly_contrib'],
            annual_rate=params['annual_rate'],
            years=params['years']
        )
        
        return {
            'success': True,
            'result': round(future_value, 2),
            'explanation': explanation,
            'parameters': params,
            'investment_type': 'monthly'
        }
        
    except Exception as e:
        return {
            'success': False,
            'result': None,
            'explanation': f"Error calculating: {str(e)}",
            'parameters': params
        }


def calculate_compound_interest(
    principal: float,
    annual_rate: float,
    years: int,
    compounds_per_year: int = 12
) -> Tuple[float, str]:
    """
    Calculate compound interest on a lump sum investment.
    
    Formula: A = P(1 + r/n)^(nt)
    
    Args:
        principal: Initial investment amount
        annual_rate: Annual interest rate as percentage
        years: Number of years
        compounds_per_year: Compounding frequency (default: 12)
        
    Returns:
        Tuple of (future_value, explanation_string)
    """
    r = annual_rate / 100
    n = compounds_per_year
    t = years
    
    # A = P(1 + r/n)^(nt)
    future_value = principal * (1 + r/n) ** (n * t)
    interest_earned = future_value - principal
    
    explanation = (
        f"Investing ${principal:,.2f} at {annual_rate}% annual return "
        f"for {years} years (compounded {compounds_per_year}x/year):\n"
        f"• Initial investment: ${principal:,.2f}\n"
        f"• Interest earned: ${interest_earned:,.2f}\n"
        f"• Final value: ${future_value:,.2f}\n"
        f"Your money will grow {future_value / principal:.2f}x!"
    )
    
    return future_value, explanation


if __name__ == "__main__":
    """
    Demo script to test the financial calculator
    """
    print("=" * 60)
    print("MoneyMentor - Financial Calculator Demo")
    print("=" * 60)
    print()
    
    # Test 1: Direct calculation
    print("Test 1: Direct Calculation")
    print("-" * 60)
    fv, explanation = calculate_future_value(500, 7, 20)
    print(explanation)
    print()
    
    # Test 2: Natural language query
    print("Test 2: Natural Language Query")
    print("-" * 60)
    query = "If I invest $1000 a month at 8% for 30 years, how much?"
    print(f"Query: {query}")
    print()
    result = run_calculation_query(query)
    if result['success']:
        print(f"✅ Success!")
        print(f"Parameters: {result['parameters']}")
        print(f"\nResult: ${result['result']:,.2f}")
        print(f"\n{result['explanation']}")
    else:
        print(f"❌ Failed: {result['explanation']}")
    print()
    
    # Test 3: Various query formats
    print("Test 3: Various Query Formats")
    print("-" * 60)
    test_queries = [
        "Invest 200 per month at 6% for 15 years",
        "$750/month at 7.5% return for 25 years",
        "500 monthly at 5% for 10 years",
    ]
    
    for query in test_queries:
        print(f"Query: {query}")
        result = run_calculation_query(query)
        if result['success']:
            print(f"  → Result: ${result['result']:,.2f}")
        else:
            print(f"  → Failed to parse")
        print()
    
    # Test 4: Compound interest (lump sum)
    print("Test 4: Lump Sum Investment")
    print("-" * 60)
    fv, explanation = calculate_compound_interest(10000, 7, 20)
    print(explanation)
    print()
    
    print("=" * 60)
    print("✅ Calculator Demo Complete!")
    print("=" * 60)

