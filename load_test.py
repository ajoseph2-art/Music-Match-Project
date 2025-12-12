#!/usr/bin/env python3
"""
Load testing script for MusicMatch application
Usage: python load_test.py <url>
Example: python load_test.py http://localhost:8000
"""

import sys
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def make_request(url):
    """Make a single HTTP request"""
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        elapsed_time = time.time() - start_time
        return {
            'status_code': response.status_code,
            'elapsed_time': elapsed_time,
            'success': response.status_code == 200
        }
    except Exception as e:
        return {
            'status_code': 0,
            'elapsed_time': 0,
            'success': False,
            'error': str(e)
        }

def load_test(url, num_requests=100, num_threads=10):
    """Run load test"""
    print("Load testing: {}".format(url))
    print("Total requests: {}".format(num_requests))
    print("Concurrent threads: {}".format(num_threads))
    print("-" * 50)
    
    start_time = time.time()
    results = []
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(make_request, url) for _ in range(num_requests)]
        
        for future in as_completed(futures):
            results.append(future.result())
    
    total_time = time.time() - start_time
    
    # Calculate statistics
    successful = sum(1 for r in results if r['success'])
    failed = num_requests - successful
    avg_time = sum(r['elapsed_time'] for r in results) / num_requests if results else 0
    min_time = min(r['elapsed_time'] for r in results if r['elapsed_time'] > 0) if results else 0
    max_time = max(r['elapsed_time'] for r in results) if results else 0
    
    status_codes = {}
    for r in results:
        code = r['status_code']
        status_codes[code] = status_codes.get(code, 0) + 1
    
    # Print results
    print("\nResults:")
    print("  Total time: {:.2f} seconds".format(total_time))
    print("  Successful requests: {}/{}".format(successful, num_requests))
    print("  Failed requests: {}/{}".format(failed, num_requests))
    print("  Requests per second: {:.2f}".format(num_requests/total_time))
    print("  Average response time: {:.3f} seconds".format(avg_time))
    print("  Min response time: {:.3f} seconds".format(min_time))
    print("  Max response time: {:.3f} seconds".format(max_time))
    print("\nStatus codes:")
    for code, count in sorted(status_codes.items()):
        print("  {}: {}".format(code, count))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python load_test.py <url> [num_requests] [num_threads]")
        print("Example: python load_test.py http://localhost:8000 100 10")
        sys.exit(1)
    
    url = sys.argv[1]
    num_requests = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    num_threads = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    
    load_test(url, num_requests, num_threads)

