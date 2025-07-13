#!/usr/bin/env python3
"""
Test script for automated evaluation of pharma-research-extractor.

This script validates that the package meets the assignment requirements:
1. Module and CLI separation
2. TestPyPI publishing readiness
"""

import sys
import subprocess
import importlib
from pathlib import Path


def test_module_import():
    """Test that the package can be imported as a module."""
    print("🔍 Testing module import...")
    
    try:
        # Test main package import
        import pharma_research_extractor
        print(f"✅ Package imported successfully")
        print(f"   Version: {pharma_research_extractor.__version__}")
        
        # Test core components
        from pharma_research_extractor import PubMedClient, OutputWriter
        print("✅ Core classes imported successfully")
        
        # Test instantiation
        client = PubMedClient()
        writer = OutputWriter()
        print("✅ Core classes instantiated successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_cli_availability():
    """Test that the CLI command is available."""
    print("\n🔍 Testing CLI availability...")
    
    try:
        # Test CLI help command
        result = subprocess.run(
            ["get-papers-list", "--help"], 
            capture_output=True, 
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ CLI command available and working")
            print("✅ Help output generated successfully")
            return True
        else:
            print(f"❌ CLI command failed with return code: {result.returncode}")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ CLI command timed out")
        return False
    except FileNotFoundError:
        print("❌ CLI command not found (entry point not installed)")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_package_structure():
    """Test that the package has the correct structure."""
    print("\n🔍 Testing package structure...")
    
    required_files = [
        "pyproject.toml",
        "README.md",
        "src/pharma_research_extractor/__init__.py",
        "src/pharma_research_extractor/cli.py",
        "src/pharma_research_extractor/pubmed_client.py",
        "src/pharma_research_extractor/output.py"
    ]
    
    all_good = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_good = False
    
    return all_good


def test_pyproject_config():
    """Test pyproject.toml configuration."""
    print("\n🔍 Testing pyproject.toml configuration...")
    
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            print("❌ Cannot test pyproject.toml - no TOML parser available")
            return False
    
    try:
        with open("pyproject.toml", "rb") as f:
            config = tomllib.load(f)
        
        # Check required fields
        project = config.get("project", {})
        
        checks = [
            ("name", project.get("name")),
            ("version", project.get("version")), 
            ("description", project.get("description")),
            ("authors", project.get("authors")),
            ("dependencies", project.get("dependencies"))
        ]
        
        all_good = True
        for field, value in checks:
            if value:
                print(f"✅ {field} configured")
            else:
                print(f"❌ {field} missing")
                all_good = False
        
        # Check scripts
        scripts = project.get("scripts", {})
        if "get-papers-list" in scripts:
            print("✅ CLI entry point configured")
        else:
            print("❌ CLI entry point missing")
            all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"❌ Error reading pyproject.toml: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("AUTOMATED EVALUATION TEST")
    print("Pharma Research Extractor")
    print("=" * 60)
    
    tests = [
        ("Package Structure", test_package_structure),
        ("PyProject Configuration", test_pyproject_config),
        ("Module Import", test_module_import),
        ("CLI Availability", test_cli_availability)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'=' * 20} {test_name} {'=' * 20}")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:.<40} {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Package meets assignment requirements")
        print("✅ Ready for automated evaluation")
        sys.exit(0)
    else:
        print(f"\n❌ {len(tests) - passed} tests failed")
        print("❌ Package needs fixes before evaluation")
        sys.exit(1)


if __name__ == "__main__":
    main()
