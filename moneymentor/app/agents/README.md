# MoneyMentor Agents

Specialized agents for different financial tasks and calculations.

## Overview

The agents module contains specialized tools that handle specific financial tasks:

- **Financial Calculator**: Investment projections, compound interest calculations
- *(Future)* Loan Calculator: Mortgage, car loans, personal loans
- *(Future)* Budget Planner: Income/expense analysis
- *(Future)* Retirement Calculator: 401k, IRA projections

---

## Available Agents

### 1. Financial Calculator Agent

**File**: `finance_calculator_agent.py`

**Purpose**: Calculate investment growth and compound interest with natural language queries.

#### Functions

##### `calculate_future_value(monthly_contrib, annual_rate, years, compounds_per_year=12)`

Calculate future value of an annuity with periodic contributions.

```python
from agents import calculate_future_value

fv, explanation = calculate_future_value(
    monthly_contrib=500,
    annual_rate=7,
    years=20
)
print(f"Future Value: ${fv:,.2f}")
# Output: Future Value: $260,463.33
```

**Parameters:**
- `monthly_contrib` (float): Monthly contribution amount
- `annual_rate` (float): Annual interest rate as percentage (e.g., 7 for 7%)
- `years` (int): Number of years to invest
- `compounds_per_year` (int): Compounding frequency (default: 12 for monthly)

**Returns:**
- Tuple of `(future_value: float, explanation: str)`

**Formula:**
```
FV = PMT × [((1 + r)^n - 1) / r]

Where:
- PMT = periodic payment (monthly contribution)
- r = interest rate per period (annual_rate / compounds_per_year)
- n = total number of periods (years × compounds_per_year)
```

---

##### `calculate_compound_interest(principal, annual_rate, years, compounds_per_year=12)`

Calculate compound interest on a lump sum investment.

```python
from agents import calculate_compound_interest

fv, explanation = calculate_compound_interest(
    principal=10000,
    annual_rate=7,
    years=20
)
print(explanation)
```

**Formula:**
```
A = P(1 + r/n)^(nt)

Where:
- P = principal (initial investment)
- r = annual interest rate (as decimal)
- n = number of times interest compounds per year
- t = number of years
```

---

##### `run_calculation_query(query)`

**High-level wrapper** that parses natural language queries and returns structured results.

```python
from agents import run_calculation_query

result = run_calculation_query(
    "If I invest $500 a month at 7% for 20 years, how much?"
)

if result['success']:
    print(f"Result: ${result['result']:,.2f}")
    print(result['explanation'])
```

**Parameters:**
- `query` (str): Natural language query about investment calculations

**Returns:**
Dictionary with:
```python
{
    'success': bool,              # True if parsing and calculation succeeded
    'result': float or None,      # Future value
    'explanation': str,            # Detailed explanation or error message
    'parameters': dict or None    # Extracted parameters
}
```

**Supported Query Formats:**

✅ **Working Examples:**
```python
"If I invest $500 a month at 7% for 20 years, how much?"
"What if I put away $200 per month at 5% for 10 years?"
"Invest 1000 monthly at 8% for 25 years"
"$1500/month at 6.5% return for 15 years"
"Save $750 a month at 6% for 30 years"
```

❌ **Will Fail (Missing Parameters):**
```python
"How much money do I need?"
"$500 a month for 20 years"  # Missing rate
"At 7% for 10 years"          # Missing contribution
```

---

##### `parse_investment_query(query)`

Lower-level parser that extracts parameters from natural language.

```python
from agents import parse_investment_query

params = parse_investment_query("Invest $500/month at 7% for 20 years")
# Returns: {'monthly_contrib': 500.0, 'annual_rate': 7.0, 'years': 20}
```

**Returns:**
- Dictionary with parameters or `None` if parsing fails

---

## Usage Examples

### Example 1: Direct Calculation

```python
from agents import calculate_future_value

# Calculate: $500/month at 7% for 20 years
future_value, explanation = calculate_future_value(500, 7, 20)

print(f"Future Value: ${future_value:,.2f}")
print(explanation)
```

**Output:**
```
Future Value: $260,463.33
Investing $500.00/month at 7% annual return for 20 years:
• Total contributions: $120,000.00
• Interest earned: $140,463.33
• Final value: $260,463.33
Your money will grow 2.17x through compound interest!
```

---

### Example 2: Natural Language Query

```python
from agents import run_calculation_query

query = "If I invest $1000 a month at 8% for 30 years, how much?"
result = run_calculation_query(query)

if result['success']:
    print(f"Result: ${result['result']:,.2f}")
    print(f"Parameters: {result['parameters']}")
    print(f"\n{result['explanation']}")
else:
    print(f"Error: {result['explanation']}")
```

**Output:**
```
Result: $1,490,359.45
Parameters: {'monthly_contrib': 1000.0, 'annual_rate': 8.0, 'years': 30}

Investing $1,000.00/month at 8.0% annual return for 30 years:
• Total contributions: $360,000.00
• Interest earned: $1,130,359.45
• Final value: $1,490,359.45
Your money will grow 4.14x through compound interest!
```

---

### Example 3: API Integration

Add calculator support to the main chat endpoint:

```python
# In app/main.py

from agents import run_calculation_query

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
                    'text': f"Calculated with parameters: {calc_result['parameters']}",
                    'relevance_score': 1.0
                }],
                query=request.question,
                model='calculator_agent'
            )
    
    # Fall back to RAG pipeline for other questions
    answer = get_finance_answer(request.question, k=request.k)
    return ChatResponse(**answer)
```

---

## Testing

### Run Built-in Tests

```bash
# Test the calculator agent directly
cd moneymentor
python app/agents/finance_calculator_agent.py

# Run integration tests
python test_calculator_agent.py
```

### Quick Test in Python

```python
from agents import run_calculation_query

# Test a query
result = run_calculation_query("$500 monthly at 7% for 20 years")
print(result)
```

---

## Edge Cases

The calculator handles various edge cases:

| Scenario | Example | Result |
|----------|---------|--------|
| Very long term | 50 years | ✅ Works |
| Zero interest | 0% rate | ✅ Works (no growth) |
| High contributions | $10,000/month | ✅ Works |
| Decimal rates | 7.25% | ✅ Works |
| Large numbers | $100,000/month | ✅ Works |
| Missing parameters | No rate specified | ❌ Returns error message |
| Invalid format | Random text | ❌ Returns helpful error |

---

## Parsing Rules

### Number Formats
- ✅ `500`, `1000`, `10000` (no commas)
- ✅ `$500`, `$1,000`, `$10,000` (with commas)
- ✅ `500.50`, `$1,234.56` (decimals)

### Rate Formats
- ✅ `7%`, `7.5%`, `at 7%`
- ✅ `7 percent`, `7.5 percent`
- ✅ `at 6.5%`, `with 8%`, `earning 5%`

### Time Periods
- ✅ `20 years`, `for 20 years`, `over 30 years`
- ✅ `in 15 years`

### Contribution Formats
- ✅ `per month`, `a month`, `monthly`, `/month`
- ✅ `each month`, `every month`

---

## Future Enhancements

### Planned Features

1. **Loan Calculator**
   ```python
   calculate_loan_payment(principal, annual_rate, years)
   # Example: Mortgage, car loan, personal loan
   ```

2. **Retirement Calculator**
   ```python
   calculate_retirement_savings(
       current_age, retirement_age, 
       current_savings, monthly_contrib, 
       annual_return
   )
   ```

3. **Budget Analyzer**
   ```python
   analyze_budget(income, expenses)
   # Categorize, suggest improvements
   ```

4. **Tax Calculator**
   ```python
   calculate_tax_savings(income, deductions)
   # Federal, state, deductions
   ```

### Enhancement Ideas

- [ ] Support for different compounding frequencies (daily, quarterly, annually)
- [ ] Inflation adjustment calculations
- [ ] Risk analysis (best/worst case scenarios)
- [ ] Goal-based calculations ("I need $X, how much to invest?")
- [ ] Visual charts (matplotlib/plotly integration)
- [ ] Export calculations to PDF report

---

## Error Handling

The agent gracefully handles errors:

```python
result = run_calculation_query("invalid query")

# Returns:
{
    'success': False,
    'result': None,
    'explanation': "I couldn't parse that query. Please try a format like...",
    'parameters': None
}
```

---

## Contributing

To add a new agent:

1. Create `app/agents/your_agent.py`
2. Implement core functions
3. Add natural language parsing if needed
4. Create demo/test script
5. Update `app/agents/__init__.py`
6. Add documentation to this README

---

## Mathematical Formulas Reference

### Future Value of Annuity (Regular Deposits)
```
FV = PMT × [((1 + r)^n - 1) / r]
```

### Compound Interest (Lump Sum)
```
A = P(1 + r/n)^(nt)
```

### Present Value
```
PV = FV / (1 + r)^n
```

### Loan Payment (Amortization)
```
PMT = [P × r(1 + r)^n] / [(1 + r)^n - 1]
```

---

## Resources

- [Future Value Formula Explanation](https://www.investopedia.com/terms/f/futurevalue.asp)
- [Compound Interest](https://www.investopedia.com/terms/c/compoundinterest.asp)
- [Time Value of Money](https://www.investopedia.com/terms/t/timevalueofmoney.asp)

---

**Built with** ❤️ **for MoneyMentor**

*Last updated: October 2025*

