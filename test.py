import unittest
import pandas as pd
from MVP import load_data, display_head, plot_annual_grants, display_descriptive_stats, validate_and_filter_data, aggregate_and_sort_data, save_data_to_excel

class TestMVPFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load data once for all tests if possible to save time
        cls.participants_df, cls.projects_df, cls.countries_df = load_data()

    def test_load_data(self):
        # Ensure dataframes are loaded correctly
        self.assertIsInstance(self.participants_df, pd.DataFrame)
        self.assertIsInstance(self.projects_df, pd.DataFrame)
        self.assertIsInstance(self.countries_df, pd.DataFrame)

    def test_display_head(self):
        # Can only manually review output or check if it does not crash
        self.assertIsNone(display_head(self.projects_df))

    def test_plot_annual_grants(self):
        # Checking if it returns a Series and plotting does not throw any error
        result = plot_annual_grants(self.projects_df)
        self.assertIsInstance(result, pd.Series)

    def test_display_descriptive_stats(self):
        # Similar to plotting, test return and output consistency
        annual_grants = self.projects_df.groupby('year')['ecMaxContribution'].sum()
        result = display_descriptive_stats(annual_grants)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(result.name, 'ecMaxContribution')

    def test_validate_and_filter_data(self):
        # Test both valid and invalid inputs
        country_acronyms = {'USA': 'US', 'France': 'FR'}
        result_valid = validate_and_filter_data(self.participants_df, 'France', country_acronyms)
        self.assertIsNotNone(result_valid)
        result_invalid = validate_and_filter_data(self.participants_df, 'Mars', country_acronyms)
        self.assertIsNone(result_invalid)

    def test_aggregate_and_sort_data(self):
        # Test data aggregation and sorting
        filtered_data = self.participants_df[self.participants_df['country'] == 'FR']
        result = aggregate_and_sort_data(filtered_data)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertFalse(result.empty)

    def test_save_data_to_excel(self):
        # Ensure function runs without error and saves file (test file existence or mock)
        sorted_data = pd.DataFrame({'name': ['Test']})
        save_data_to_excel(sorted_data, 'test_output.xlsx')
        import os
        self.assertTrue(os.path.exists('test_output.xlsx'))
        os.remove('test_output.xlsx')  # Clean up after test

if __name__ == '__main__':
    unittest.main()