#!/usr/bin/env python3
"""
Simple test script to verify all modules work correctly
"""

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
        
        import matplotlib.pyplot as plt
        print("✅ matplotlib imported successfully")
        
        import sklearn
        print("✅ sklearn imported successfully")
        
        import plotly
        print("✅ plotly imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_csv_loading():
    """Test that the CSV file can be loaded"""
    try:
        import pandas as pd
        df = pd.read_csv("sample_expenses.csv")
        print(f"✅ CSV loaded successfully: {len(df)} rows")
        print(f"   Columns: {list(df.columns)}")
        return True
    except Exception as e:
        print(f"❌ CSV loading error: {e}")
        return False

def test_modules():
    """Test that our custom modules can be imported"""
    try:
        from visualize import create_charts
        print("✅ visualize module imported successfully")
        
        from predict import predict_next_month
        print("✅ predict module imported successfully")
        
        from analysis import load_and_clean_data
        print("✅ analysis module imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Module import error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Budget & Expense Analysis Setup...")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("CSV Loading", test_csv_loading),
        ("Custom Modules", test_modules)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed!")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready to run the analysis.")
        print("\n🚀 Next steps:")
        print("   1. Run: python analysis.py")
        print("   2. Check the 'charts' directory for generated visualizations")
        print("   3. View the interactive plotly dashboard: charts/plotly_dashboard.html")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
