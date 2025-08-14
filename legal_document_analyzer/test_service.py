"""Test service agreement clause extraction."""

from streamlit_app import StandaloneLegalAnalyzer

def test_service_agreement():
    """Test clause extraction with service agreement."""
    analyzer = StandaloneLegalAnalyzer()
    result = analyzer.analyze_document('sample_service_agreement.txt', max_clauses=15)

    print('📄 Service Agreement Analysis:')
    print(f'Total Clauses Found: {result["clauses"]["total_count"]}')
    print(f'Clauses Processed: {len(result["clauses"]["simplified_clauses"])}')
    print()

    for i, clause in enumerate(result['clauses']['simplified_clauses']):
        preview = clause['original_clause'][:80] + '...' if len(clause['original_clause']) > 80 else clause['original_clause']
        print(f'{i+1}. {preview}')
        print(f'   Summary: {clause["plain_english_summary"]}')
        print()

if __name__ == "__main__":
    test_service_agreement()