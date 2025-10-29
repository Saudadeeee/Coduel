#!/usr/bin/env python3
"""Debug script to understand Kattis HTML structure"""
from kattis_scrape import fetch_problem_html
import re

slug = "carrots"
print(f"Fetching {slug}...")
soup = fetch_problem_html(slug)

print("\n" + "="*60)
print("LOOKING FOR SAMPLE DATA SECTIONS")
print("="*60)

# Find all tables (Kattis uses tables for samples)
tables = soup.find_all("table", class_=re.compile(r"sample"))
print(f"\nFound {len(tables)} sample tables")
for i, table in enumerate(tables):
    print(f"\nTable {i+1}:")
    print(f"  Classes: {table.get('class')}")
    pre_tags = table.find_all("pre")
    print(f"  Pre tags: {len(pre_tags)}")
    for j, pre in enumerate(pre_tags):
        content = pre.get_text().strip()
        print(f"    Pre {j+1}: {content[:50]}...")

# Look for sample headings
print("\n" + "="*60)
print("LOOKING FOR HEADINGS")
print("="*60)
for tag in soup.find_all(['h2', 'h3', 'h4']):
    text = tag.get_text().strip()
    if 'sample' in text.lower() or 'input' in text.lower() or 'output' in text.lower():
        print(f"\n{tag.name}: {text}")
        # Look at next siblings
        for i, sibling in enumerate(tag.next_siblings):
            if i > 3:  # Only check first few siblings
                break
            if hasattr(sibling, 'name') and sibling.name:
                print(f"  → {sibling.name}: {sibling.get_text()[:80] if sibling.get_text() else 'empty'}...")

# Check for sample data in specific divs
print("\n" + "="*60)
print("LOOKING FOR SAMPLE DIVS")
print("="*60)
for div in soup.find_all("div", class_=re.compile(r"sample", re.I)):
    print(f"\nDiv classes: {div.get('class')}")
    pres = div.find_all("pre")
    for pre in pres:
        print(f"  Content: {pre.get_text()[:100]}")
