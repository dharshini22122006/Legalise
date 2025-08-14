"""Debug clause extraction."""

import re

def debug_clause_extraction():
    """Debug the clause extraction process."""
    
    # Read the complex contract
    with open('complex_contract.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    print("📄 Original text length:", len(text))
    print("📄 First 500 characters:")
    print(text[:500])
    print("\n" + "="*50)
    
    # Test Method 1: Numbered sections
    print("🔍 Testing Method 1: Numbered sections")
    numbered_sections = re.split(r'\n\s*(\d+)\.\s+([A-Z][A-Z\s]+)\n', text)
    print(f"Found {len(numbered_sections)} parts")
    for i, part in enumerate(numbered_sections[:10]):  # Show first 10 parts
        print(f"Part {i}: {repr(part[:100])}")
    
    print("\n" + "="*50)
    
    # Test Method 2: Simple numbered pattern
    print("🔍 Testing Method 2: Simple numbered pattern")
    lines = text.split('\n')
    numbered_lines = []
    for i, line in enumerate(lines):
        line = line.strip()
        match = re.match(r'^(\d+)\.\s+(.+)', line)
        if match:
            numbered_lines.append((i, match.group(1), match.group(2)))
    
    print(f"Found {len(numbered_lines)} numbered lines:")
    for line_num, num, content in numbered_lines:
        print(f"Line {line_num}: {num}. {content[:50]}...")
    
    print("\n" + "="*50)
    
    # Test Method 3: Paragraph splitting
    print("🔍 Testing Method 3: Paragraph splitting")
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    print(f"Found {len(paragraphs)} paragraphs:")
    for i, para in enumerate(paragraphs[:5]):
        print(f"Paragraph {i+1}: {para[:100]}...")

if __name__ == "__main__":
    debug_clause_extraction()