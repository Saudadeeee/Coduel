#!/usr/bin/env python3
"""
Token-based output comparison with floating-point tolerance.
"""
import sys


def is_integer_token(s):
    """Check if a string represents a plain integer (no decimal point, no exponent)."""
    try:
        int(s)
        return '.' not in s and 'e' not in s.lower()
    except ValueError:
        return False


def is_float_token(s):
    """Check if a string represents a floating-point number (has decimal point or exponent)."""
    try:
        float(s)
        return '.' in s or 'e' in s.lower()
    except ValueError:
        return False


def compare_outputs(user_file, expected_file, epsilon=1e-6):
    """
    Compare outputs token by token.
    - Ignores whitespace differences
    - For integer tokens: exact match required (no tolerance)
    - For float tokens (contains '.' or 'e'): accepts if |user - expected| <= epsilon or relative <= epsilon
    - For non-numeric strings: exact match required
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
        # Integer expected: require exact string match (no float tolerance)
        if is_integer_token(expected_token):
            if user_token != expected_token:
                print("WA")
                sys.exit(1)
        # Float expected: allow small epsilon tolerance
        elif is_float_token(expected_token):
            try:
                user_val = float(user_token)
                expected_val = float(expected_token)
                abs_diff = abs(user_val - expected_val)
                rel_diff = abs_diff / abs(expected_val) if expected_val != 0 else abs_diff
                if abs_diff > epsilon and rel_diff > epsilon:
                    print("WA")
                    sys.exit(1)
            except ValueError:
                print("WA")
                sys.exit(1)
        # Non-numeric: exact match
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
