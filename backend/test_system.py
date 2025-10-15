#!/usr/bin/env python3
"""
Simple test script to verify the Knowledge Base Search Engine is working correctly.
Run this after starting the server to ensure everything is operational.

Usage:
    python test_system.py
"""

import requests
import sys
import time

BASE_URL = "http://127.0.0.1:8000"
COLORS = {
    'green': '\033[92m',
    'red': '\033[91m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'reset': '\033[0m'
}

def colored(text, color):
    """Return colored text for terminal output."""
    return f"{COLORS.get(color, '')}{text}{COLORS['reset']}"

def print_section(title):
    """Print a section header."""
    print(f"\n{colored('━' * 60, 'blue')}")
    print(f"{colored(title, 'blue')}")
    print(f"{colored('━' * 60, 'blue')}\n")

def test_connection():
    """Test if the server is reachable."""
    print("Testing server connection...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print(colored("✅ Server is running", "green"))
            return True
        else:
            print(colored(f"❌ Server returned status {response.status_code}", "red"))
            return False
    except requests.exceptions.ConnectionError:
        print(colored("❌ Cannot connect to server", "red"))
        print(colored("   Make sure server is running: uvicorn app.main:app --reload", "yellow"))
        return False
    except Exception as e:
        print(colored(f"❌ Error: {e}", "red"))
        return False

def test_health_check():
    """Test the health check endpoint."""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        data = response.json()
        
        print(f"   Status: {colored(data['status'], 'green')}")
        print(f"   Documents loaded: {colored(data['docs_loaded'], 'green')}")
        
        if data['docs_loaded'] == 0:
            print(colored("   ⚠️  Warning: No documents loaded!", "yellow"))
            print(colored("   Add .txt or .pdf files to backend/app/docs/", "yellow"))
        else:
            print(colored(f"   ✅ {data['docs_loaded']} documents ready", "green"))
        
        return True
    except Exception as e:
        print(colored(f"❌ Health check failed: {e}", "red"))
        return False

def test_stats():
    """Test the stats endpoint."""
    print("Testing stats endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/stats")
        data = response.json()
        
        print(f"   Total documents: {colored(data['total_documents'], 'green')}")
        print(f"   Index size: {colored(data['index_size'], 'green')}")
        print(f"   Embedding model: {colored(data['model'], 'green')}")
        print(colored("   ✅ Stats endpoint working", "green"))
        return True
    except Exception as e:
        print(colored(f"❌ Stats test failed: {e}", "red"))
        return False

def test_query(query_text):
    """Test a search query."""
    print(f"Testing query: '{colored(query_text, 'blue')}'")
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/search",
            json={"query": query_text, "top_k": 3}
        )
        end_time = time.time()
        
        if response.status_code != 200:
            print(colored(f"❌ Query failed with status {response.status_code}", "red"))
            return False
        
        data = response.json()
        response_time = (end_time - start_time) * 1000  # Convert to ms
        
        print(f"   Response time: {colored(f'{response_time:.0f}ms', 'green')}")
        print(f"   Sources found: {colored(len(data['sources']), 'green')}")
        
        if data['sources']:
            for i, source in enumerate(data['sources'][:2], 1):
                similarity = source['similarity'] * 100
                print(f"   Source {i}: {colored(source['file'], 'blue')} "
                      f"(Similarity: {colored(f'{similarity:.1f}%', 'green')})")
        
        # Check answer quality
        answer_length = len(data['answer'])
        if answer_length < 50:
            print(colored("   ⚠️  Warning: Answer is very short", "yellow"))
        else:
            print(colored(f"   ✅ Answer generated ({answer_length} chars)", "green"))
        
        return True
    except Exception as e:
        print(colored(f"❌ Query test failed: {e}", "red"))
        return False

def test_error_handling():
    """Test error handling with invalid inputs."""
    print("Testing error handling...")
    try:
        # Test empty query
        response = requests.post(
            f"{BASE_URL}/search",
            json={"query": ""}
        )
        if response.status_code == 400:
            print(colored("   ✅ Empty query handled correctly", "green"))
        else:
            print(colored("   ⚠️  Empty query should return 400", "yellow"))
        
        # Test missing query field
        response = requests.post(
            f"{BASE_URL}/search",
            json={}
        )
        if response.status_code in [400, 422]:
            print(colored("   ✅ Missing query handled correctly", "green"))
        else:
            print(colored("   ⚠️  Missing query should return error", "yellow"))
        
        return True
    except Exception as e:
        print(colored(f"❌ Error handling test failed: {e}", "red"))
        return False

def main():
    """Run all tests."""
    print(colored("\n" + "=" * 60, "blue"))
    print(colored("   🧪 Knowledge Base Search Engine - System Test", "blue"))
    print(colored("=" * 60, "blue"))
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Connection
    print_section("Test 1: Server Connection")
    if test_connection():
        tests_passed += 1
    else:
        tests_failed += 1
        print(colored("\n❌ Cannot proceed without server connection", "red"))
        sys.exit(1)
    
    # Test 2: Health Check
    print_section("Test 2: Health Check")
    if test_health_check():
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 3: Statistics
    print_section("Test 3: Statistics Endpoint")
    if test_stats():
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Test 4: Sample Queries
    print_section("Test 4: Search Queries")
    
    sample_queries = [
        "What is HTTP?",
        "Explain primary key",
        "What is normalization?"
    ]
    
    for query in sample_queries:
        if test_query(query):
            tests_passed += 1
        else:
            tests_failed += 1
        print()  # Blank line between queries
    
    # Test 5: Error Handling
    print_section("Test 5: Error Handling")
    if test_error_handling():
        tests_passed += 1
    else:
        tests_failed += 1
    
    # Summary
    print_section("Test Summary")
    total_tests = tests_passed + tests_failed
    print(f"Total tests: {total_tests}")
    print(f"{colored(f'Passed: {tests_passed}', 'green')}")
    if tests_failed > 0:
        print(f"{colored(f'Failed: {tests_failed}', 'red')}")
    
    success_rate = (tests_passed / total_tests) * 100 if total_tests > 0 else 0
    print(f"\nSuccess rate: {colored(f'{success_rate:.1f}%', 'green' if success_rate == 100 else 'yellow')}")
    
    if tests_failed == 0:
        print(colored("\n🎉 All tests passed! System is working correctly.", "green"))
        print(colored("\nNext steps:", "blue"))
        print("  1. Open frontend/index.html in your browser")
        print("  2. Try searching for questions")
        print("  3. Check the sources and similarity scores")
        return 0
    else:
        print(colored("\n⚠️  Some tests failed. Check the output above for details.", "yellow"))
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(colored("\n\n⚠️  Tests interrupted by user", "yellow"))
        sys.exit(1)
    except Exception as e:
        print(colored(f"\n\n❌ Unexpected error: {e}", "red"))
        sys.exit(1)

