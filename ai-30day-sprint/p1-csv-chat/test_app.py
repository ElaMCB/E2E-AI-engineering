import os
import pytest
import pandas as pd
from app import load_csv, query_data

# Sample test data
def create_test_csv(filename: str = "test_data.csv"):
    data = {
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['New York', 'San Francisco', 'Los Angeles']
    }
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    return filename

def test_load_csv():
    """Test loading a CSV file."""
    test_file = create_test_csv()
    try:
        result = load_csv(test_file)
        assert "successfully" in result.lower()
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)

def test_query_data():
    """Test querying the loaded data."""
    test_file = create_test_csv()
    try:
        # Load test data
        load_csv(test_file)
        
        # Test a simple query
        result = query_data("What are the column names?")
        assert "name" in result.lower()
        assert "age" in result.lower()
        assert "city" in result.lower()
        
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    pytest.main(["-v", "test_app.py"])
