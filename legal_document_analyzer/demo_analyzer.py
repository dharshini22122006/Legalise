"""Demo version of the legal document analyzer showcasing efficiency improvements."""

import asyncio
import time
import threading
from typing import Dict, Any, List
from concurrent.futures import ThreadPoolExecutor
import json

class MockModel:
    """Mock model for demonstration purposes."""
    
    def __init__(self):
        self.load_time = 2.0  # Simulate 2-second model loading
        self._loaded = False
    
    def load(self):
        if not self._loaded:
            print(f"🔄 Loading model... (simulating {self.load_time}s)")
            time.sleep(self.load_time)
            self._loaded = True
            print("✅ Model loaded successfully")
    
    def process(self, text: str, task: str) -> Dict[str, Any]:
        """Simulate model processing."""
        processing_time = len(text) / 1000  # Simulate processing time based on text length
        time.sleep(processing_time)
        
        return {
            'task': task,
            'text_length': len(text),
            'processing_time': processing_time,
            'result': f"Processed {task} for {len(text)} characters"
        }

class OriginalAnalyzer:
    """Original analyzer implementation (inefficient)."""
    
    def __init__(self):
        self.model = MockModel()
        self.model.load()  # Load model on every instance
    
    def analyze_document(self, text: str) -> Dict[str, Any]:
        """Synchronous document analysis."""
        print("🐌 Running original analyzer...")
        start_time = time.time()
        
        # Sequential processing
        classification = self.model.process(text, "classification")
        entities = self.model.process(text, "entity_extraction")
        clauses = self.model.process(text, "clause_extraction")
        simplification = self.model.process(text, "simplification")
        
        total_time = time.time() - start_time
        
        return {
            'method': 'original',
            'total_time': total_time,
            'results': [classification, entities, clauses, simplification]
        }

class OptimizedAnalyzer:
    """Optimized analyzer implementation."""
    
    _instance = None
    _lock = threading.Lock()
    _model = None
    
    def __new__(cls):
        """Singleton pattern to avoid multiple model loadings."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        # Load model only once
        if OptimizedAnalyzer._model is None:
            OptimizedAnalyzer._model = MockModel()
            OptimizedAnalyzer._model.load()
        
        self.model = OptimizedAnalyzer._model
        self.executor = ThreadPoolExecutor(max_workers=4)
        self._initialized = True
    
    async def analyze_document(self, text: str) -> Dict[str, Any]:
        """Asynchronous document analysis with parallel processing."""
        print("🚀 Running optimized analyzer...")
        start_time = time.time()
        
        # Parallel processing using asyncio
        loop = asyncio.get_event_loop()
        
        tasks = [
            loop.run_in_executor(self.executor, self.model.process, text, "classification"),
            loop.run_in_executor(self.executor, self.model.process, text, "entity_extraction"),
            loop.run_in_executor(self.executor, self.model.process, text, "clause_extraction"),
            loop.run_in_executor(self.executor, self.model.process, text, "simplification")
        ]
        
        results = await asyncio.gather(*tasks)
        
        total_time = time.time() - start_time
        
        return {
            'method': 'optimized',
            'total_time': total_time,
            'results': results
        }

class PerformanceBenchmark:
    """Performance benchmarking utility."""
    
    def __init__(self):
        self.results = []
    
    def run_benchmark(self, sample_texts: List[str]):
        """Run performance benchmark comparing both analyzers."""
        print("🏁 Starting Performance Benchmark")
        print("=" * 60)
        
        for i, text in enumerate(sample_texts, 1):
            print(f"\n📄 Test Document {i} ({len(text)} characters)")
            print("-" * 40)
            
            # Test original analyzer
            original_analyzer = OriginalAnalyzer()
            original_result = original_analyzer.analyze_document(text)
            
            # Test optimized analyzer
            optimized_analyzer = OptimizedAnalyzer()
            optimized_result = asyncio.run(optimized_analyzer.analyze_document(text))
            
            # Calculate improvement
            improvement = ((original_result['total_time'] - optimized_result['total_time']) 
                          / original_result['total_time']) * 100
            
            result = {
                'document': i,
                'text_length': len(text),
                'original_time': original_result['total_time'],
                'optimized_time': optimized_result['total_time'],
                'improvement_percent': improvement
            }
            
            self.results.append(result)
            
            print(f"⏱️  Original: {original_result['total_time']:.2f}s")
            print(f"⚡ Optimized: {optimized_result['total_time']:.2f}s")
            print(f"📈 Improvement: {improvement:.1f}%")
        
        self.print_summary()
    
    def print_summary(self):
        """Print benchmark summary."""
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE BENCHMARK SUMMARY")
        print("=" * 60)
        
        total_original = sum(r['original_time'] for r in self.results)
        total_optimized = sum(r['optimized_time'] for r in self.results)
        overall_improvement = ((total_original - total_optimized) / total_original) * 100
        
        print(f"📄 Documents tested: {len(self.results)}")
        print(f"⏱️  Total original time: {total_original:.2f}s")
        print(f"⚡ Total optimized time: {total_optimized:.2f}s")
        print(f"📈 Overall improvement: {overall_improvement:.1f}%")
        
        avg_improvement = sum(r['improvement_percent'] for r in self.results) / len(self.results)
        print(f"📊 Average improvement: {avg_improvement:.1f}%")
        
        print("\n🎯 Key Optimizations Demonstrated:")
        print("   ✅ Singleton pattern for model loading")
        print("   ✅ Parallel processing with asyncio")
        print("   ✅ ThreadPoolExecutor for CPU-bound tasks")
        print("   ✅ Reduced redundant operations")

def main():
    """Main demonstration function."""
    print("⚖️ Legal Document Analyzer - Efficiency Demo")
    print("=" * 60)
    
    # Sample legal document texts of varying lengths
    sample_texts = [
        # Short document
        """This Non-Disclosure Agreement (NDA) is entered into between Company A and Company B. 
        The parties agree to maintain confidentiality of all shared information.""",
        
        # Medium document
        """EMPLOYMENT AGREEMENT
        
        This Employment Agreement is made between XYZ Corporation and John Doe.
        
        1. POSITION AND DUTIES
        Employee shall serve as Software Engineer and perform duties including:
        - Software development and maintenance
        - Code review and testing
        - Documentation and reporting
        
        2. COMPENSATION
        Employee shall receive a salary of $75,000 per year, payable bi-weekly.
        
        3. BENEFITS
        Employee is entitled to health insurance, dental coverage, and 401(k) matching.
        
        4. TERMINATION
        Either party may terminate this agreement with 30 days written notice.""",
        
        # Large document
        """SERVICE AGREEMENT
        
        This Service Agreement is entered into between ABC Services Inc. and Client Corp.
        
        1. SCOPE OF WORK
        Provider agrees to deliver the following services:
        - Web application development using modern frameworks
        - Database design and implementation
        - User interface design and user experience optimization
        - Quality assurance testing and bug fixes
        - Deployment and maintenance services
        - Technical documentation and training
        
        2. TIMELINE AND DELIVERABLES
        The project shall be completed in phases:
        Phase 1: Requirements gathering and system design (4 weeks)
        Phase 2: Backend development and database setup (6 weeks)
        Phase 3: Frontend development and integration (8 weeks)
        Phase 4: Testing, deployment, and documentation (4 weeks)
        
        3. PAYMENT TERMS
        Total project cost is $150,000, payable as follows:
        - 25% upon signing this agreement
        - 25% upon completion of Phase 1
        - 25% upon completion of Phase 2
        - 25% upon final delivery and acceptance
        
        4. INTELLECTUAL PROPERTY
        All work products shall be owned by Client Corp upon full payment.
        Provider retains rights to general methodologies and know-how.
        
        5. CONFIDENTIALITY
        Both parties agree to maintain strict confidentiality of proprietary information.
        This obligation survives termination of this agreement.
        
        6. LIABILITY AND INDEMNIFICATION
        Provider's liability is limited to the total contract value.
        Client agrees to indemnify Provider against third-party claims.""" * 2  # Double the text for larger size
    ]
    
    # Run benchmark
    benchmark = PerformanceBenchmark()
    benchmark.run_benchmark(sample_texts)
    
    print("\n🎉 Demo completed! The optimized analyzer shows significant improvements.")
    print("💡 In a real implementation with heavy ML models, improvements would be even greater.")

if __name__ == "__main__":
    main()