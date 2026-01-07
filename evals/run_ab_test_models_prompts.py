"""
A/B Testing Framework for LLM Agents

This script demonstrates how to run A/B tests comparing different models,
prompts, and tool configurations for agent evaluation.

Usage:
    python run_ab_test_models_prompts.py --config eval_config_examples.yaml
"""

import json
import yaml
import argparse
from typing import Dict, List, Any
from dataclasses import dataclass
from pathlib import Path
import time
from datetime import datetime

@dataclass
class TestVariant:
    """Represents a single test variant (model + prompt + tools)"""
    name: str
    model: str
    prompt_version: str
    tools: List[str]
    
@dataclass
class TestResult:
    """Results for a single test case"""
    variant: str
    test_case_id: str
    input: str
    output: str
    correctness: float
    latency_ms: float
    safety_score: float
    timestamp: str

class ABTestRunner:
    """Runs A/B tests across multiple agent configurations"""
    
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.variants = self._load_variants()
        self.results: List[TestResult] = []
    
    def _load_variants(self) -> List[TestVariant]:
        """Load test variants from config"""
        variants = []
        for variant_config in self.config['ab_tests']['variants']:
            variant = TestVariant(
                name=variant_config['name'],
                model=variant_config['model'],
                prompt_version=variant_config['prompt_version'],
                tools=variant_config.get('tools', [])
            )
            variants.append(variant)
        return variants
    
    def run_test_case(self, test_case: Dict[str, Any], variant: TestVariant) -> TestResult:
        """
        Run a single test case with a specific variant.
        
        In a real implementation, this would:
        1. Load the prompt for this variant
        2. Call the LLM API with the test input
        3. Measure latency
        4. Evaluate correctness and safety
        """
        start_time = time.time()
        
        # Placeholder: In real implementation, call LLM API
        output = f"[Mock output for {variant.name} on test case {test_case['id']}]"
        
        latency_ms = (time.time() - start_time) * 1000
        
        # Placeholder: In real implementation, evaluate correctness
        correctness = 0.85  # Mock score
        
        # Placeholder: In real implementation, evaluate safety
        safety_score = 0.92  # Mock score
        
        return TestResult(
            variant=variant.name,
            test_case_id=test_case['id'],
            input=test_case['input'],
            output=output,
            correctness=correctness,
            latency_ms=latency_ms,
            safety_score=safety_score,
            timestamp=datetime.now().isoformat()
        )
    
    def run_ab_test(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run A/B test across all variants and test cases"""
        sample_size = self.config['ab_tests']['sample_size_per_variant']
        
        print(f"Running A/B test with {len(self.variants)} variants")
        print(f"Sample size per variant: {sample_size}")
        print(f"Total test cases: {len(test_cases)}")
        
        for variant in self.variants:
            print(f"\nTesting variant: {variant.name}")
            for i, test_case in enumerate(test_cases[:sample_size]):
                result = self.run_test_case(test_case, variant)
                self.results.append(result)
                if (i + 1) % 10 == 0:
                    print(f"  Completed {i + 1}/{sample_size} test cases")
        
        return self._analyze_results()
    
    def _analyze_results(self) -> Dict[str, Any]:
        """Analyze results and compute statistics"""
        analysis = {}
        
        for variant in self.variants:
            variant_results = [r for r in self.results if r.variant == variant.name]
            
            if variant_results:
                analysis[variant.name] = {
                    'sample_size': len(variant_results),
                    'avg_correctness': sum(r.correctness for r in variant_results) / len(variant_results),
                    'avg_latency_ms': sum(r.latency_ms for r in variant_results) / len(variant_results),
                    'avg_safety_score': sum(r.safety_score for r in variant_results) / len(variant_results),
                    'min_correctness': min(r.correctness for r in variant_results),
                    'max_correctness': max(r.correctness for r in variant_results),
                }
        
        return analysis
    
    def save_results(self, output_path: str):
        """Save results to JSON file"""
        results_dict = {
            'config': self.config,
            'results': [
                {
                    'variant': r.variant,
                    'test_case_id': r.test_case_id,
                    'input': r.input,
                    'output': r.output,
                    'correctness': r.correctness,
                    'latency_ms': r.latency_ms,
                    'safety_score': r.safety_score,
                    'timestamp': r.timestamp
                }
                for r in self.results
            ],
            'analysis': self._analyze_results()
        }
        
        with open(output_path, 'w') as f:
            json.dump(results_dict, f, indent=2)
        
        print(f"\nResults saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Run A/B tests for LLM agents')
    parser.add_argument('--config', type=str, default='eval_config_examples.yaml',
                       help='Path to evaluation config YAML file')
    parser.add_argument('--test-cases', type=str, default='test_cases.json',
                       help='Path to test cases JSON file')
    parser.add_argument('--output', type=str, default='ab_test_results.json',
                       help='Output path for results')
    
    args = parser.parse_args()
    
    # Load test cases
    # In a real implementation, load from file or generate programmatically
    test_cases = [
        {'id': f'test_{i}', 'input': f'Test input {i}'}
        for i in range(200)
    ]
    
    # Run A/B test
    runner = ABTestRunner(args.config)
    analysis = runner.run_ab_test(test_cases)
    
    # Print summary
    print("\n" + "="*60)
    print("A/B Test Results Summary")
    print("="*60)
    for variant_name, stats in analysis.items():
        print(f"\n{variant_name}:")
        print(f"  Average Correctness: {stats['avg_correctness']:.3f}")
        print(f"  Average Latency: {stats['avg_latency_ms']:.2f} ms")
        print(f"  Average Safety Score: {stats['avg_safety_score']:.3f}")
    
    # Save results
    runner.save_results(args.output)

if __name__ == '__main__':
    main()

