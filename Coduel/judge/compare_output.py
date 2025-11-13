#!/usr/bin/env python3
"""
Simple token-based output comparison (whitespace-insensitive).
"""
import sys


def compare_outputs(user_file, expected_file):
    """
    Compare outputs token by token.
    Ignores whitespace differences - flexible and simple.
    """
    try:
        with open(user_file, 'r', encoding='utf-8') as f:
            user_output = f.read()
        with open(expected_file, 'r', encoding='utf-8') as f:
            expected_output = f.read()
    except Exception as e:
        print(f"Error reading files: {e}", file=sys.stderr)
        sys.exit(2)
    
    # Split into tokens (whitespace-insensitive)
    user_tokens = user_output.split()
    expected_tokens = expected_output.split()
    
    # Compare token by token
    if user_tokens == expected_tokens:
        print("OK")
        sys.exit(0)
    else:
        print("WA")
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: compare_output.py <user_output> <expected_output>", file=sys.stderr)
        sys.exit(2)
    
    compare_outputs(sys.argv[1], sys.argv[2])
