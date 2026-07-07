#!/usr/bin/env python3
"""
Generate metrics JSON files for badges.
This script is run by CI to generate coverage.json and eval.json.
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Dict, Any
import subprocess
import os

def calculate_coverage(coverage_dir: Path) -> Dict[str, Any]:
    """Calculate overall coverage from multiple coverage.json files."""
    total_covered = 0
    coverage_files = []
    
    # Find all coverage.json files
    if coverage_dir and coverage_dir.exists():
        coverage_files = list(coverage_dir.rglob("coverage.json"))
        print(f"Found {len(coverage_files)} coverage files in {coverage_dir}", file=sys.stderr)
    else:
        print(f"Coverage directory does not exist: {coverage_dir}", file=sys.stderr)
    
    # Also check for coverage.xml files (coverage.py can generate both)
    if coverage_dir and coverage_dir.exists():
        xml_files = list(coverage_dir.rglob("coverage.xml"))
        if xml_files and not coverage_files:
            # If we have XML but no JSON, try to parse XML
            # For now, return a placeholder - in production, parse XML
            print("Found coverage.xml files but no JSON. Using placeholder.", file=sys.stderr)
    
    # Aggregate coverage from all projects
    valid_coverage_files = []
    if coverage_files:
        for cov_file in coverage_files:
            try:
                with open(cov_file, 'r') as f:
                    data = json.load(f)
                    percent = 0.0
                    # Coverage.py JSON format (pytest-cov)
                    if 'totals' in data:
                        percent = data['totals'].get('percent_covered', 0.0)
                    elif 'percent_covered' in data:
                        percent = data['percent_covered']
                    elif isinstance(data, dict) and 'coverage' in data:
                        percent = data['coverage']
                    
                    # Check if this is a real coverage file (not a fallback)
                    # Real coverage files have 'files' key even if coverage is 0%
                    # Fallback files only have 'totals' with no 'files' key
                    has_files_key = 'files' in data
                    has_totals_key = 'totals' in data
                    
                    # Count as valid if:
                    # 1. Has actual coverage data (files key) - even if 0%
                    # 2. OR has percent > 0 (real coverage, might not have files key in some formats)
                    if has_files_key or percent > 0.0:
                        total_covered += percent
                        valid_coverage_files.append(cov_file)
                        print(f"Found coverage from {cov_file}: {percent:.1f}% (has_files={has_files_key})", file=sys.stderr)
                    else:
                        # This is likely a fallback file created when tests didn't run
                        print(f"Skipping {cov_file}: appears to be a fallback (0% with no file data, has_files={has_files_key}, has_totals={has_totals_key})", file=sys.stderr)
            except Exception as e:
                print(f"Error reading {cov_file}: {e}", file=sys.stderr)
    
    # Average coverage across projects with valid data, or default to 0
    if valid_coverage_files:
        avg_coverage = total_covered / len(valid_coverage_files)
        coverage_percent = round(avg_coverage, 1)
        print(f"Averaged coverage from {len(valid_coverage_files)} project(s): {coverage_percent}%", file=sys.stderr)
    else:
        avg_coverage = 0.0
        coverage_percent = 0.0
        print("No valid coverage data found (all projects may have skipped tests or no coverage generated)", file=sys.stderr)
    
    # Determine color
    if coverage_percent >= 80:
        color = "green"
    elif coverage_percent >= 60:
        color = "yellow"
    elif coverage_percent >= 40:
        color = "orange"
    else:
        color = "red"
    
    return {
        "schemaVersion": 1,
        "label": "Coverage",
        "message": f"{coverage_percent}%",
        "color": color
    }

def run_evaluation_tests() -> Dict[str, Any]:
    """Run evaluation tests and return metrics."""
    original_dir = os.getcwd()
    try:
        # Check if evals directory exists
        evals_dir = Path("evals")
        if not evals_dir.exists():
            print("evals directory not found", file=sys.stderr)
            return {
                "schemaVersion": 1,
                "label": "Eval Score",
                "message": "N/A",
                "color": "grey"
            }
        
        # Run the actual A/B test evaluation
        result = subprocess.run(
            [sys.executable, "evals/run_ab_test_models_prompts.py", "--quick"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=original_dir
        )
        
        print(f"Eval output: {result.stdout}", file=sys.stderr)
        if result.stderr:
            print(f"Eval stderr: {result.stderr}", file=sys.stderr)
        
        if result.returncode == 0:
            # Parse the eval score from output
            # Look for "Eval Score: XX.X%"
            import re
            match = re.search(r'Eval Score:\s*([\d.]+)%', result.stdout)
            if match:
                score = float(match.group(1))
                
                # Determine color based on score
                if score >= 85:
                    color = "green"
                elif score >= 70:
                    color = "yellow"
                elif score >= 50:
                    color = "orange"
                else:
                    color = "red"
                
                return {
                    "schemaVersion": 1,
                    "label": "Eval Score",
                    "message": f"{score:.1f}%",
                    "color": color
                }
            else:
                print("Eval script completed but no parseable score was found", file=sys.stderr)
                return {
                    "schemaVersion": 1,
                    "label": "Eval Score",
                    "message": "N/A",
                    "color": "grey"
                }
        else:
            print(f"Eval script failed: {result.stderr}", file=sys.stderr)
            return {
                "schemaVersion": 1,
                "label": "Eval Score",
                "message": "N/A",
                "color": "grey"
            }
    except subprocess.TimeoutExpired:
        print("Eval script timed out", file=sys.stderr)
        return {
            "schemaVersion": 1,
            "label": "Eval Score",
            "message": "N/A",
            "color": "grey"
        }
    except Exception as e:
        print(f"Error running evals: {e}", file=sys.stderr)
        return {
            "schemaVersion": 1,
            "label": "Eval Score",
            "message": "N/A",
            "color": "grey"
        }
    finally:
        os.chdir(original_dir)

def main():
    parser = argparse.ArgumentParser(description='Generate metrics JSON for badges')
    parser.add_argument('--coverage-dir', type=str, help='Directory containing coverage artifacts')
    parser.add_argument('--run-evals', action='store_true', help='Run evaluation tests')
    parser.add_argument('--output', type=str, required=True, help='Output JSON file path')
    
    args = parser.parse_args()
    
    output_path = Path(args.output)
    
    if args.coverage_dir:
        coverage_data = calculate_coverage(Path(args.coverage_dir))
        with open(output_path, 'w') as f:
            json.dump(coverage_data, f, indent=2)
        print(f"Generated {output_path} with coverage: {coverage_data['message']}")
    
    if args.run_evals:
        eval_data = run_evaluation_tests()
        with open(output_path, 'w') as f:
            json.dump(eval_data, f, indent=2)
        print(f"Generated {output_path} with eval score: {eval_data['message']}")

if __name__ == '__main__':
    main()

