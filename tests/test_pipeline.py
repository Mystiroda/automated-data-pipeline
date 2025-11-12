#!/usr/bin/env python3
"""
Test Script for Automated Data Pipeline
Run: python test_pipeline.py
"""

import pytest
import pandas as pd
import sqlite3
from pathlib import Path
import sys
import os

sys.path.insert(0, str(Path(__file__).parent))

from src.data_downloader import download_dataset, load_downloaded_data
from src.data_cleaner import clean_dataframe, clean_dataset
from src.database_handler import dataframe_to_sqlite, list_tables, run_sql_query
from src.data_analyzer import analyze_data
from src.plot_generator import generate_all_plots


class TestDataPipeline:
    """Test cases for the data pipeline components"""

    def setup_method(self):
        """Setup test environment"""
        self.test_data_dir = Path("test_data")
        self.test_data_dir.mkdir(exist_ok=True)

        # sample test data
        self.sample_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', None, 'Eve'],
            'age': [25, 30, None, 40, 35],
            'score': [85.5, 92.0, 78.5, None, 88.0],
            'category': ['A', 'B', 'A', 'C', 'B']
        })

        self.sample_csv_path = self.test_data_dir / "test_data.csv"
        self.sample_data.to_csv(self.sample_csv_path, index=False)

    def teardown_method(self):
        """Clean up test files"""
        import shutil
        if Path("test_data").exists():
            shutil.rmtree("test_data")
        if Path("test_outputs").exists():
            shutil.rmtree("test_outputs")

    def test_data_loading(self):
        """Test that data can be loaded from CSV"""
        df = load_downloaded_data(self.sample_csv_path)
        assert df is not None
        assert len(df) == 5
        assert 'name' in df.columns

    def test_data_cleaning(self):
        """Test data cleaning functionality"""
        df_clean = clean_dataframe(self.sample_data)

        assert df_clean is not None
        assert df_clean['name'].isna().sum() == 0
        assert df_clean['age'].isna().sum() == 0
        assert len(df_clean) == 5

    def test_database_operations(self):
        """Test database storage and retrieval"""
        table_name = dataframe_to_sqlite(self.sample_data, "test_table")

        assert table_name is not None
        assert "test_table" in list_tables()

        # Test query
        result = run_sql_query("SELECT COUNT(*) as count FROM test_table")
        assert result is not None
        assert result.iloc[0]['count'] == 5

    def test_data_analysis(self):
        """Test data analysis functionality"""
        analysis_results = analyze_data(self.sample_data)

        assert analysis_results is not None
        assert 'shape' in analysis_results
        assert analysis_results['shape'] == (5, 5)
        assert 'numeric_stats' in analysis_results

    def test_plot_generation(self):
        """Test plot generation (should not crash)"""
        # This just tests that plots can be generated without errors
        try:
            plot_count = generate_all_plots(self.sample_data)
            assert isinstance(plot_count, int)
        except Exception as e:
            pytest.fail(f"Plot generation failed: {e}")


def test_integration():
    """Integration test for the complete pipeline"""
    from main import run_pipeline

    # Test with a dataset
    test_url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

    try:
        result = run_pipeline(dataset_url=test_url, dataset_name='iris')
        assert isinstance(result, bool)
    except Exception as e:
        pytest.fail(f"Integration test failed: {e}")


def test_file_structure():
    """Test that required directories are created"""
    required_dirs = [
        "data/raw",
        "data/processed",
        "outputs/plots",
        "outputs/reports"
    ]

    for dir_path in required_dirs:
        assert Path(dir_path).exists(), f"Directory {dir_path} should exist"


if __name__ == "__main__":
    # Run tests
    print("🧪 Running Data Pipeline Tests...")
    print("=" * 50)

    # Create test instance
    test_class = TestDataPipeline()

    try:
        test_class.setup_method()

        print("Testing data loading...")
        test_class.test_data_loading()
        print("Data loading test passed!")

        print("Testing data cleaning...")
        test_class.test_data_cleaning()
        print("Data cleaning test passed!")

        print("Testing database operations...")
        test_class.test_database_operations()
        print("Database operations test passed!")

        print("Testing data analysis...")
        test_class.test_data_analysis()
        print("Data analysis test passed!")

        print("Testing plot generation...")
        test_class.test_plot_generation()
        print("Plot generation test passed!")

        print("Testing file structure...")
        test_file_structure()
        print("File structure test passed!")

        print("Testing integration...")
        test_integration()
        print("Integration test passed!")

        print("\n All tests passed!!!")

    except Exception as e:
        print(f"Test failed: {e}")
        raise
    finally:
        test_class.teardown_method()