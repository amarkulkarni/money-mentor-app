#!/usr/bin/env python3
"""Check if LangSmith has MoneyMentor runs."""

import os
from dotenv import load_dotenv

load_dotenv()

try:
    from langsmith import Client
    
    client = Client()
    
    # Get recent runs for MoneyMentor project
    print("🔍 Checking LangSmith for MoneyMentor runs...")
    print("=" * 60)
    
    runs = list(client.list_runs(
        project_name="MoneyMentor",
        limit=20
    ))
    
    if runs:
        print(f"✅ Found {len(runs)} runs in LangSmith!")
        print()
        print("Recent runs:")
        for i, run in enumerate(runs[:5], 1):
            print(f"  {i}. {run.name}")
            print(f"     Created: {run.start_time}")
            if run.inputs:
                query = run.inputs.get('query', 'N/A')
                print(f"     Query: {query[:60]}...")
            print()
        
        print(f"🎉 LangSmith is working!")
        print()
        print("View all runs:")
        print(f"  https://smith.langchain.com/o/default/projects/p/MoneyMentor")
    else:
        print("❌ No runs found in LangSmith")
        print()
        print("This could mean:")
        print("  1. Tracing is not enabled (check LANGCHAIN_TRACING_V2=true)")
        print("  2. API key is wrong")
        print("  3. Runs are in a different project")
        print("  4. Project name mismatch (check LANGCHAIN_PROJECT)")
        
except Exception as e:
    print(f"❌ Error connecting to LangSmith: {e}")
    print()
    print("Make sure:")
    print("  - LANGCHAIN_API_KEY is set correctly")
    print("  - You have internet connection")
    print("  - Your API key is valid")

