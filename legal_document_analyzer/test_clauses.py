"""Test the enhanced clause extraction."""

from streamlit_app import StandaloneLegalAnalyzer

def test_clause_extraction():
    """Test clause extraction with the complex contract."""
    print("🔍 Testing Enhanced Clause Extraction")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = StandaloneLegalAnalyzer()
    
    # Test with complex contract
    print("📄 Testing with complex_contract.txt...")
    try:
        result = analyzer.analyze_document('complex_contract.txt', max_clauses=15)
        
        print("✅ Analysis completed!")
        print(f"📋 Document Type: {result['classification']['predicted_type']}")
        print(f"📊 Confidence: {result['classification']['confidence']:.1%}")
        print(f"📝 Word Count: {result['text_statistics']['word_count']}")
        print(f"🔍 Total Clauses Found: {result['clauses']['total_count']}")
        print(f"📄 Clauses Processed: {len(result['clauses']['simplified_clauses'])}")
        
        print("\n📋 Clause Breakdown:")
        for i, clause_data in enumerate(result['clauses']['simplified_clauses']):
            clause_preview = clause_data['original_clause'][:100] + "..." if len(clause_data['original_clause']) > 100 else clause_data['original_clause']
            print(f"  {i+1}. {clause_preview}")
        
        print(f"\n🎯 Sample Simplifications:")
        for i, clause_data in enumerate(result['clauses']['simplified_clauses'][:3]):
            print(f"\nClause {i+1} Summary: {clause_data['plain_english_summary']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎉 Clause extraction test completed!")

if __name__ == "__main__":
    test_clause_extraction()