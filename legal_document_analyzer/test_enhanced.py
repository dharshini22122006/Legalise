"""Test the enhanced legal document analyzer."""

from streamlit_app import StandaloneLegalAnalyzer

def test_enhanced_analyzer():
    """Test the enhanced analyzer functionality."""
    print("🔍 Testing Enhanced Legal Document Analyzer")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = StandaloneLegalAnalyzer()
    
    # Test supported formats
    print("📁 Supported Formats:")
    for fmt, available in analyzer.supported_formats.items():
        status = "✅" if available else "❌"
        print(f"  {status} {fmt.upper()}")
    
    print()
    
    # Test document analysis
    print("📄 Testing document analysis...")
    try:
        result = analyzer.analyze_document('sample_service_agreement.txt')
        
        print("✅ Analysis completed!")
        print(f"📋 Document Type: {result['classification']['predicted_type']}")
        print(f"📊 Confidence: {result['classification']['confidence']:.1%}")
        print(f"📝 Word Count: {result['text_statistics']['word_count']}")
        print(f"🔍 Entities Found: {result['entities']['total_entities']}")
        print(f"📄 Clauses Processed: {len(result['clauses']['simplified_clauses'])}")
        
        # Show first simplified clause
        if result['clauses']['simplified_clauses']:
            first_clause = result['clauses']['simplified_clauses'][0]
            print(f"\n🎯 First Clause Summary: {first_clause['plain_english_summary']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎉 Enhanced analyzer test completed!")

if __name__ == "__main__":
    test_enhanced_analyzer()