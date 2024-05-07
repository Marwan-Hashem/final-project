import pandas as pd
import matplotlib.pyplot as plt

# Load data from Excel
def load_data():
    participants_df = pd.read_excel('participants.xlsx')
    projects_df = pd.read_excel('projects.xlsx')
    countries_df = pd.read_excel('countries.xlsx')
    return participants_df, projects_df, countries_df

# Display head of each DataFrame
def display_head(df):
    print(df.head())

# Calculate and plot annual grants
def plot_annual_grants(projects_df):
    annual_grants = projects_df.groupby('year')['ecMaxContribution'].sum()
    plt.figure(figsize=(10, 6))
    annual_grants.plot(kind='bar', color='skyblue')
    plt.title('Total Annual Received Grants')
    plt.xlabel('Year')
    plt.ylabel('EC Contribution (€)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    return annual_grants

# Generate and display descriptive statistics
def display_descriptive_stats(annual_grants):
    stats = annual_grants.describe()
    print("Descriptive Statistics for Annual Grants:")
    print(stats)
    return stats

# Validate country input and filter data
def validate_and_filter_data(participants_df, country_name, country_acronyms):
    if country_name in country_acronyms:
        print("Valid country entered:", country_name)
        selected_country_acronym = country_acronyms[country_name]
        filtered_participants = participants_df[participants_df['country'] == selected_country_acronym]
        return filtered_participants
    else:
        print("Invalid country. Please enter a valid country name.")
        return None

# Aggregate and sort country-specific data
def aggregate_and_sort_data(filtered_participants):
    aggregated_data = filtered_participants.groupby(['shortName', 'name', 'activityType', 'organizationURL']).agg(
        sum_ecContribution=('ecContribution', 'sum'),
        count_project=('projectID', 'nunique'),
        count_coordinator=('role', lambda x: (x == 'coordinator').sum())
    ).reset_index()
    sorted_data = aggregated_data.sort_values(by='sum_ecContribution', ascending=False)
    return sorted_data

# Save sorted data to an Excel file
def save_data_to_excel(sorted_data, filename):
    sorted_data.to_excel(filename, index=False, sheet_name='Summary')

def main():
    participants_df, projects_df, countries_df = load_data()
    display_head(participants_df)
    display_head(projects_df)
    display_head(countries_df)

    annual_grants = plot_annual_grants(projects_df)
    display_descriptive_stats(annual_grants)

    country_acronyms = {
        'Belgium': 'BE', 'Bulgaria': 'BG', 'Spain': 'ES', 'France': 'FR',
        'Germany': 'DE', 'Italy': 'IT', 'Netherlands': 'NL', 'Poland': 'PL'
    }
    
    user_input = input("Please enter a country name: ").title()
    filtered_participants = validate_and_filter_data(participants_df, user_input, country_acronyms)
    
    if filtered_participants is not None:
        sorted_data = aggregate_and_sort_data(filtered_participants)
        print(sorted_data)
        save_data_to_excel(sorted_data, 'output_country_data.xlsx')

if __name__ == '__main__':
    main()