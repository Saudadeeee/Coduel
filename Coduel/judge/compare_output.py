#!/usr/bin/env python3
"""
Token-based output comparison with floating-point tolerance.
"""
import sys


def is_number(s):
    """Check if a string represents a number."""
    try:
        float(s)
        return True
    except ValueError:
        return False


def compare_outputs(user_file, expected_file, epsilon=1e-4):
    """
    Compare outputs token by token.
    - Ignores whitespace differences
    - For numbers: accepts if |user - expected| <= epsilon or relative error <= epsilon
    - For strings: exact match required
    """
    try:
        with open(user_file, 'r', encoding='utf-8') as f:
            user_output = f.read()
        with open(expected_file, 'r', encoding='utf-8') as f:
            expected_output = f.read()
    except Exception as e:
        print(f"Error reading files: {e}", file=sys.stderr)
        sys.exit(2)
    
    user_tokens = user_output.split()
    expected_tokens = expected_output.split()
    
    if len(user_tokens) != len(expected_tokens):
        print("WA")
        sys.exit(1)
    
    for user_token, expected_token in zip(user_tokens, expected_tokens):
        if is_number(user_token) and is_number(expected_token):
            user_val = float(user_token)
            expected_val = float(expected_token)
            
            abs_diff = abs(user_val - expected_val)
            
            if expected_val != 0:
                rel_diff = abs_diff / abs(expected_val)
            else:
                rel_diff = abs_diff
            
            if abs_diff > epsilon and rel_diff > epsilon:
                print("WA")
                sys.exit(1)
        else:
            if user_token != expected_token:
                print("WA")
                sys.exit(1)
    
    print("OK")
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: compare_output.py <user_output> <expected_output>", file=sys.stderr)
        sys.exit(2)
    
    compare_outputs(sys.argv[1], sys.argv[2])
